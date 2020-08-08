# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

"""

"""

from .exclude import ExcludeSchema, rating_indices
from .spec import SpecSchema, loadspec, savespec
from .tags import BoldTagsSchema, entities, entity_longnames
from .file import (
    File,
    BidsFileSchema,
    AnatFileSchema,
    T1wFileSchema,
    FuncFileSchema,
    BoldFileSchema,
    TxtEventsFileSchema,
    TsvEventsFileSchema,
    MatEventsFileSchema,
    FmapFileSchema,
    PhaseFmapFileSchema,
    PhaseDiffFmapFileSchema,
    EPIFmapFileSchema,
    BaseFmapFileSchema,
    RefFileSchema,
    SpreadsheetFileSchema,
    FileSchema,
)
from .setting import (
    SettingSchema,
    BaseSettingSchema,
    SmoothingSettingSchema,
    BandpassFilterSettingSchema,
    GrandMeanScalingSettingSchema,
)
from .metadata import MetadataSchema, direction_codes, axis_codes, space_codes
from .resultdict import ResultdictSchema
from .filter import FilterSchema, GroupFilterSchema, TagFilterSchema
from .contrast import TContrastSchema, InferredTypeContrastSchema
from .model import (
    Model,
    ModelSchema,
    FixedEffectsModelSchema,
    MixedEffectsModelSchema,
    LinearMixedEffectsModelSchema,
)
from .feature import Feature, FeatureSchema
from .variable import VariableSchema

__all__ = [
    ExcludeSchema,
    rating_indices,
    SpecSchema,
    loadspec,
    savespec,
    BoldTagsSchema,
    entities,
    entity_longnames,
    File,
    BidsFileSchema,
    AnatFileSchema,
    T1wFileSchema,
    FuncFileSchema,
    BoldFileSchema,
    TxtEventsFileSchema,
    TsvEventsFileSchema,
    MatEventsFileSchema,
    FmapFileSchema,
    PhaseFmapFileSchema,
    PhaseDiffFmapFileSchema,
    EPIFmapFileSchema,
    BaseFmapFileSchema,
    RefFileSchema,
    FileSchema,
    SettingSchema,
    BaseSettingSchema,
    SmoothingSettingSchema,
    BandpassFilterSettingSchema,
    GrandMeanScalingSettingSchema,
    MetadataSchema,
    direction_codes,
    axis_codes,
    space_codes,
    ResultdictSchema,
    FilterSchema,
    GroupFilterSchema,
    TagFilterSchema,
    TContrastSchema,
    InferredTypeContrastSchema,
    Model,
    ModelSchema,
    FixedEffectsModelSchema,
    MixedEffectsModelSchema,
    LinearMixedEffectsModelSchema,
    SpreadsheetFileSchema,
    VariableSchema,
    Feature,
    FeatureSchema,
]
