# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import logging
from uuid import uuid5
import pickle
from pathlib import Path

from ..interface import AggregateResultdicts, MakeResultdicts
from ..database import Database
from ..spec import loadspec, study_entities
from ..utils import cacheobj, uncacheobj
from ..io import get_repetition_time
from .utils import make_resultdict_datasink

from nipype.pipeline import engine as pe

from .fmriprepwrapper import (
    init_anat_preproc_wf,
    init_func_preproc_wf,
    connect_func_wf_attrs_from_anat_preproc_wf,
    get_fmaps,
)
from .firstlevel import init_firstlevel_analysis_wf, connect_firstlevel_analysis_extra_args
from .higherlevel import init_higherlevel_analysis_wf
from .filt import (
    init_bold_filt_wf,
    connect_filt_wf_attrs_from_anat_preproc_wf,
    connect_filt_wf_attrs_from_func_preproc_wf,
)
from .memory import memcalc_from_database

analysisoutattr = "outputnode.resultdicts"


class Cache:
    def __init__(self):
        self._cache = {}

    def get(self, func, argtuples=None):
        if argtuples is None:
            key = repr(func)
        else:
            key = (repr(func), tuple(argtuples))
        if key not in self._cache:
            kwargs = {}
            if argtuples is not None:
                kwargs = dict(list(argtuples))
                # print([(key, hash(arg)) for key, arg in kwargs.items()])
            obj = func(**kwargs)
            # print([(key, hash(arg)) for key, arg in kwargs.items()])
            self._cache[key] = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        return pickle.loads(self._cache[key])


class Formatter:
    def __init__(self, tmpl=None):
        self.tmpl = tmpl

    def __call__(self, **kwargs):
        return self.tpl.format(**kwargs)


class Pipeline:
    def __init__(self):
        pass


def init_workflow(workdir):
    """
    initialize nipype workflow

    :param spec
    """

    logger = logging.getLogger("pipeline")

    spec = loadspec(workdir=workdir)
    database = Database(files=spec.files)
    uuid = uuid5(spec.uuid, database.sha1())

    workflow = uncacheobj(workdir, "workflow", uuid)
    if workflow is not None:
        return workflow

    # create workflow
    workflow = pe.Workflow(name="nipype", base_dir=workdir)
    workflow.uuid = uuid
    uuidstr = str(uuid)[:8]
    logger.info(f"New workflow: {uuidstr}")
    workflow.config["execution"].update(
        {"crashdump_dir": workflow.base_dir, "poll_sleep_duration": 2}
    )

    # dirs
    statsdirectory = Path(workdir) / "stats"
    intermediatesdirectory = Path(workdir) / "intermediates"

    # helpers
    memcalc = memcalc_from_database(database)
    cache = Cache()

    subjectlevelworkflow = pe.Workflow(name=f"subjectlevel")
    workflow.add_nodes([subjectlevelworkflow])

    firstlevel_analyses = [analysis for analysis in spec.analyses if analysis.level == "first"]
    firstlevel_analysis_tagdicts = [
        analysis.tags.get_tagdict(study_entities) for analysis in firstlevel_analyses
    ]

    subjectlevel_analyses = [
        analysis
        for analysis in spec.analyses
        if analysis.level == "higher" and analysis.across != "subject"
    ]

    grouplevel_analyses = [
        analysis
        for analysis in spec.analyses
        if analysis.level == "higher" and analysis.across == "subject"
    ]

    analysisendpoints = {analysis.name: [] for analysis in spec.analyses}

    subjects = database.get_tagval_set("subject")
    for subject in subjects:
        subjectfiles = database.get(subject=subject)

        subjectworkflow = pe.Workflow(name=f"_subject_{subject}_")
        subjectlevelworkflow.add_nodes([subjectworkflow])

        t1wfiles = database.filter(subjectfiles, datatype="anat", suffix="T1w")
        nt1wfiles = len(t1wfiles)
        t1wfile = t1wfiles.pop()
        if nt1wfiles > 1:
            logger.warn(
                f'Found {nt1wfiles} T1w files for subject "{subject}", using "{t1wfile}"'
            )
        anat_preproc_wf = cache.get(init_anat_preproc_wf)
        anat_preproc_wf.get_node("inputnode").inputs.t1w = t1wfile

        boldfiles = database.filter(subjectfiles, datatype="func", suffix="bold")
        subjectanalysisendpoints = {analysis.name: [] for analysis in spec.analyses}
        for boldfile in boldfiles:
            boldfilemetadata = {"subject": subject}
            # make name
            name = "_bold_"
            for entity in study_entities:
                value = database.get_tagval(boldfile, entity)
                if value is not None:
                    name += f"{entity}_{value}_"
                    boldfilemetadata[entity] = value

            boldfileworkflow = pe.Workflow(name=name)

            fmap_type, fmaps, fmapmetadata = get_fmaps(boldfile, database)
            boldfilemetadata.update(fmapmetadata)

            repetition_time = database.get_tagval(boldfile, "repetition_time")
            if repetition_time is None:
                repetition_time = get_repetition_time(boldfile)
            boldfilemetadata["RepetitionTime"] = repetition_time

            func_preproc_wf = cache.get(
                init_func_preproc_wf,
                argtuples=[("fmap_type", fmap_type), ("memcalc", memcalc)],
            )
            boldfileworkflow.add_nodes([func_preproc_wf])
            func_preproc_inputnode = func_preproc_wf.get_node("inputnode")
            func_preproc_inputnode.inputs.bold_file = boldfile
            func_preproc_inputnode.inputs.fmaps = fmaps
            func_preproc_inputnode.inputs.metadata = boldfilemetadata
            connect_func_wf_attrs_from_anat_preproc_wf(
                subjectworkflow,
                anat_preproc_wf,
                boldfileworkflow,
                in_nodename=f"{func_preproc_wf.name}.inputnode",
            )

            bold_filt_wf_by_variant_dict = dict()

            def get_variant_bold_filt_wf(variant):
                if variant in bold_filt_wf_by_variant_dict:
                    return bold_filt_wf_by_variant_dict[variant]
                else:
                    bold_filt_wf = cache.get(
                        init_bold_filt_wf,
                        argtuples=[("variant", variant), ("memcalc", memcalc)],
                    )
                    boldfileworkflow.add_nodes([bold_filt_wf])
                    bold_filt_wf.get_node("inputnode").inputs.metadata = boldfilemetadata
                    connect_filt_wf_attrs_from_anat_preproc_wf(
                        subjectworkflow,
                        anat_preproc_wf,
                        boldfileworkflow,
                        in_nodename=f"{bold_filt_wf.name}.inputnode",
                    )
                    connect_filt_wf_attrs_from_func_preproc_wf(
                        boldfileworkflow, func_preproc_wf, bold_filt_wf
                    )
                    bold_filt_wf_by_variant_dict[variant] = bold_filt_wf
                    return bold_filt_wf

            variant_to_output = (
                ("space", "mni"),
                ("smoothed", 6.0),
                ("confounds_removed", ("aroma_motion_[0-9]+",)),
                ("band_pass_filtered", ("gaussian", 128.0)),
            )
            bold_filt_wf = get_variant_bold_filt_wf(variant_to_output)
            preprocresultdict = pe.Node(
                interface=MakeResultdicts(keys=["preproc", "mask_file"]),
                name="preprocresultdict",
            )
            preprocresultdict.inputs.basedict = boldfilemetadata
            boldfileworkflow.connect(
                bold_filt_wf, "outputnode.out1", preprocresultdict, "preproc",
            )
            make_resultdict_datasink(
                boldfileworkflow,
                intermediatesdirectory,
                (preprocresultdict, "resultdicts"),
                name=f"preprocdatasink",
            )

            for analysis, tagdict in zip(firstlevel_analyses, firstlevel_analysis_tagdicts):
                if not database.matches(boldfile, **tagdict):
                    continue
                analysisworkflow, boldfilevariants = cache.get(
                    init_firstlevel_analysis_wf,
                    argtuples=[("analysis", analysis), ("memcalc", memcalc)],
                )
                analysisworkflow.get_node("inputnode").inputs.metadata = boldfilemetadata
                #
                endpoint = (boldfileworkflow, f"{analysisworkflow.name}.{analysisoutattr}")
                subjectanalysisendpoints[analysis.name].append(endpoint)
                make_resultdict_datasink(
                    boldfileworkflow,
                    intermediatesdirectory,
                    (analysisworkflow, analysisoutattr),
                    name=f"{analysisworkflow.name}_resultdictdatasink",
                )
                # 1 mask_file
                boldfileworkflow.connect(
                    func_preproc_wf,
                    "outputnode.bold_mask_std",
                    analysisworkflow,
                    "inputnode.mask_file",
                )
                # 2 bold_file and confounds
                for attrnames, variant in boldfilevariants:
                    bold_filt_wf = get_variant_bold_filt_wf(variant)
                    for i, attrname in enumerate(attrnames):
                        boldfileworkflow.connect(
                            bold_filt_wf,
                            f"outputnode.out{i+1}",
                            analysisworkflow,
                            f"inputnode.{attrname}",
                        )
                # 3 type specific
                connect_firstlevel_analysis_extra_args(
                    analysisworkflow, analysis, database, boldfile
                )
        # subjectlevel aggregate
        for analysis in subjectlevel_analyses:
            endpoints = sum(
                (
                    subjectanalysisendpoints[inputanalysisname]
                    for inputanalysisname in analysis.input
                ),
                [],
            )
            collectinputs = pe.Node(
                AggregateResultdicts(numinputs=len(endpoints), across=analysis.across),
                name=f"collectinputs_{analysis.name}",
            )
            for i, endpoint in enumerate(endpoints):
                subjectworkflow.connect(*endpoint, collectinputs, f"in{i+1}")
            analysisworkflow = cache.get(
                init_higherlevel_analysis_wf,
                argtuples=[("analysis", analysis), ("memcalc", memcalc)],
            )
            subjectworkflow.connect(
                collectinputs, "resultdicts", analysisworkflow, "inputnode.indicts"
            )
            endpoint = (subjectworkflow, f"{analysisworkflow.name}.{analysisoutattr}")
            subjectanalysisendpoints[analysis.name].append(endpoint)
            make_resultdict_datasink(
                subjectworkflow,
                intermediatesdirectory,
                (analysisworkflow, analysisoutattr),
                name=f"{analysisworkflow.name}_resultdictdatasink",
            )
        for analysisname, endpoints in subjectanalysisendpoints.items():
            for endpoint in endpoints:
                node, attr = endpoint
                attr = f"{node.name}.{attr}"
                if node is not subjectworkflow:
                    attr = f"{subjectworkflow.name}.{attr}"
                analysisendpoints[analysisname].append((subjectlevelworkflow, attr))

    grouplevelworkflow = pe.Workflow(name=f"grouplevel")

    for analysis in grouplevel_analyses:
        endpoints = sum(
            (analysisendpoints[inputanalysisname] for inputanalysisname in analysis.input), [],
        )
        collectinputs = pe.Node(
            AggregateResultdicts(numinputs=len(endpoints), across=analysis.across),
            name=f"collectinputs_{analysis.name}",
        )
        grouplevelworkflow.add_nodes([collectinputs])
        for i, endpoint in enumerate(endpoints):
            workflow.connect(*endpoint, grouplevelworkflow, f"{collectinputs.name}.in{i+1}")
        analysisworkflow = cache.get(
            init_higherlevel_analysis_wf,
            argtuples=[("analysis", analysis), ("memcalc", memcalc)],
        )
        grouplevelworkflow.connect(
            collectinputs, "resultdicts", analysisworkflow, "inputnode.indicts"
        )
        endpoint = (grouplevelworkflow, f"{analysisworkflow.name}.{analysisoutattr}")
        analysisendpoints[analysis.name].append(endpoint)
        make_resultdict_datasink(
            grouplevelworkflow,
            statsdirectory,
            (analysisworkflow, analysisoutattr),
            name=f"{analysisworkflow.name}_resultdictdatasink",
        )

    cacheobj(workdir, "workflow", workflow)
    return workflow
