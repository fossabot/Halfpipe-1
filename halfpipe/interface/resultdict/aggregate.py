# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np

from nipype.interfaces.base import traits, DynamicTraitedSpec, BaseInterfaceInputSpec, isdefined
from nipype.interfaces.io import add_traits, IOBase

from .base import ResultdictsOutputSpec
from ...model import entities, ResultdictSchema
from ...utils import ravel


def _aggregate_if_possible(inval):
    if isinstance(inval, (list, tuple)):
        if all(isinstance(val, float) for val in inval):
            return np.asarray(inval).mean()
        if len(set(inval)) == 1:
            (aggval,) = inval
            return aggval
    return inval


class AggregateResultdictsInputSpec(DynamicTraitedSpec, BaseInterfaceInputSpec):
    across = traits.Str(desc="across which entity to aggregate")
    include = traits.Dict(
        traits.Str(),
        traits.List(traits.Str()),
        desc="include only resultdicts that have one of the allowed values for the respective key",
    )


class AggregateResultdicts(IOBase):
    input_spec = AggregateResultdictsInputSpec
    output_spec = ResultdictsOutputSpec

    def __init__(self, numinputs=0, **inputs):
        super(AggregateResultdicts, self).__init__(**inputs)
        self._numinputs = numinputs
        if numinputs >= 1:
            input_names = [f"in{i+1}" for i in range(numinputs)]
            add_traits(self.inputs, input_names)
        else:
            input_names = []

    def _list_outputs(self):
        outputs = self._outputs().get()

        inputs = ravel([getattr(self.inputs, f"in{i+1}") for i in range(self._numinputs)])

        across = self.inputs.across
        assert across in entities, f'Cannot aggregate across "{across}"'

        include = {}
        if isdefined(self.inputs.include):
            include = self.inputs.include

        aggdicts = {}
        for resultdict in inputs:
            resultdict = ResultdictSchema().load(resultdict)

            tags = resultdict["tags"]

            if across not in tags:
                continue

            if any(
                key not in tags or tags[key] not in allowedvalues
                for key, allowedvalues in include.items()
            ):
                continue

            tagtupl = tuple(
                (key, value)
                for key, value in tags.items()
                if key != across
                and not isinstance(value, (tuple, list))  # Ignore lists, as they only
                # will be there if we aggregated before, meaning that this is not
                # a tag that separates different results anymore.
                # This is important for example if we want have aggregated unequal numbers
                # of runs across subjects, but we still want to compare across subjects
            )

            if tagtupl not in aggdicts:
                aggdicts[tagtupl] = {}

            aggdict = aggdicts[tagtupl]

            for f, nested in resultdict.items():
                if f == "tags":
                    continue
                if f not in aggdict:
                    aggdict[f] = dict()
                for k, v in nested.items():
                    if k not in aggdict:
                        aggdict[f][k] = []
                    aggdict[f][k].append(v)

        resultdicts = []
        for tagtupl, listdict in aggdict.items():
            resultdict = dict(tagtupl)
            resultdict.update(listdict)  # create combined resultdict
            for key in resultdict.keys():  # calculate mean of floats
                resultdict[key] = _aggregate_if_possible(resultdict[key])
            resultdicts.append(ResultdictSchema().load(resultdict))

        outputs["resultdicts"] = resultdicts

        return outputs
