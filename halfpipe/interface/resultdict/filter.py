# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np

from .base import ResultdictsOutputSpec
from ...io import ExcludeDatabase, loadspreadsheet
from ...model import ResultdictSchema

from nipype.interfaces.base import (
    traits,
    BaseInterfaceInputSpec,
    SimpleInterface,
    isdefined,
)


def _aggregate_if_needed(inval):
    if isinstance(inval, (list, tuple)):
        return np.asarray(inval).mean()
    return float(inval)


def _get_categorical_dict(filepath, variableobjs):
    rawdataframe = loadspreadsheet(filepath)
    for variableobj in variableobjs:
        if variableobj.get("type") == "id":
            id_column = variableobj.get("name")
            break

    rawdataframe = rawdataframe.set_index(id_column)

    categorical_columns = []
    for variableobj in variableobjs:
        if variableobj.get("type") == "categorical":
            categorical_columns.append(variableobj.get("name"))

    return rawdataframe[categorical_columns].to_dict()


class FilterResultdictsInputSpec(BaseInterfaceInputSpec):
    indicts = traits.List(traits.Dict(traits.Str(), traits.Any()), mandatory=True)
    filterdicts = traits.List(traits.Any(), desc="filter list", mandatory=True)
    variableobjs = traits.List(traits.Any(), desc="variable list")
    spreadsheet = traits.File(desc="spreadsheet")
    requireoneofimages = traits.List(
        traits.Str(), desc="only keep resultdicts that have at least one of these keys"
    )
    excludefiles = traits.List(traits.File())


class FilterResultdicts(SimpleInterface):
    input_spec = FilterResultdictsInputSpec
    output_spec = ResultdictsOutputSpec

    def _run_interface(self, runtime):
        outdicts = self.inputs.indicts.copy()

        resultdict_schema = ResultdictSchema()
        outdicts = [resultdict_schema.load(outdict) for outdict in outdicts]  # validate

        categorical_dict = None

        for filterdict in self.inputs.filterdicts:
            action = filterdict.get("action")

            filtertype = filterdict.get("type")
            if filtertype == "group":
                if categorical_dict is None:
                    assert isdefined(self.inputs.spreadsheet)
                    assert isdefined(self.inputs.variableobjs)
                    categorical_dict = _get_categorical_dict(
                        self.inputs.spreadsheet, self.inputs.variableobjs
                    )

                variable = filterdict.get("variable")
                if variable not in categorical_dict:
                    continue

                levels = filterdict.get("levels")
                if levels is None or len(levels) == 0:
                    continue

                variable_dict = categorical_dict[variable]
                selectedsubjects = set(
                    subject for subject, value in variable_dict.items() if value in levels
                )

                if action == "include":
                    outdicts = [
                        outdict
                        for outdict in outdicts
                        if outdict.get("tags").get("sub") in selectedsubjects
                    ]
                elif action == "exclude":
                    outdicts = [
                        outdict
                        for outdict in outdicts
                        if outdict.get("tags").get("sub") not in selectedsubjects
                    ]
                else:
                    raise ValueError(f'Invalid action "{action}"')

            elif filtertype == "cutoff":

                assert action == "exclude"

                cutoff = filterdict.get("cutoff")
                if cutoff is None or not isinstance(cutoff, float):
                    raise ValueError(f'Invalid cutoff "{cutoff}"')

                outdicts = [
                    outdict
                    for outdict in outdicts
                    if _aggregate_if_needed(outdict.get("vals").get(filtertype, np.inf)) < cutoff
                ]

        if isdefined(self.inputs.requireoneofimages):
            requireoneofimages = self.inputs.requireoneofimages
            if len(requireoneofimages) > 0:
                outdicts = [
                    outdict
                    for outdict in outdicts
                    if any(
                        requireoneofkey in outdict.get("images")
                        for requireoneofkey in requireoneofimages
                    )
                ]

        if isdefined(self.inputs.excludefiles):
            database = ExcludeDatabase.cached(self.inputs.excludefiles)
            outdicts = [
                outdict for outdict in outdicts if database.get(**outdict.get("tags")) is False
            ]

        self._results["resultdicts"] = outdicts

        return runtime
