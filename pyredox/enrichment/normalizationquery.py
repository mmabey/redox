# -*- coding: utf-8 -*-
# ----  AUTO-GENERATED BY redox_lib_gen. DO NOT MODIFY MANUALLY!!  ---- #

from typing import List, Union

from pydantic import Field

from ..abstract_base import EventTypeAbstractModel, RedoxAbstractModel
from ..field_types import Number


class NormalizationQuery(EventTypeAbstractModel):
    Entries: List["NormalizationQueryEntry"] = Field(...)
    Meta: "NormalizationQueryMeta" = Field(...)


class NormalizationQueryEntry(RedoxAbstractModel):
    Category: str = Field(...)
    Code: Union[str, None] = Field(None)
    Codeset: Union[str, None] = Field(None)
    Description: Union[str, None] = Field(None)
    EntryID: Union[str, None] = Field(None)


class NormalizationQueryMeta(RedoxAbstractModel):
    DataModel: str = Field(...)
    Destinations: List["NormalizationQueryMetaDestination"] = Field(None)
    EventDateTime: Union[str, None] = Field(None)
    EventType: str = Field(...)
    FacilityCode: Union[str, None] = Field(None)
    Logs: List["NormalizationQueryMetaLog"] = Field(None)
    Message: "NormalizationQueryMetaMessage" = Field(None)
    Source: "NormalizationQueryMetaSource" = Field(None)
    Test: Union[bool, None] = Field(None)
    Transmission: "NormalizationQueryMetaTransmission" = Field(None)


class NormalizationQueryMetaDestination(RedoxAbstractModel):
    ID: Union[str, None] = Field(None)
    Name: Union[str, None] = Field(None)


class NormalizationQueryMetaLog(RedoxAbstractModel):
    AttemptID: Union[str, None] = Field(None)
    ID: Union[str, None] = Field(None)


class NormalizationQueryMetaMessage(RedoxAbstractModel):
    ID: Union[Number, None] = Field(None)


class NormalizationQueryMetaSource(RedoxAbstractModel):
    ID: Union[str, None] = Field(None)
    Name: Union[str, None] = Field(None)


class NormalizationQueryMetaTransmission(RedoxAbstractModel):
    ID: Union[Number, None] = Field(None)


NormalizationQuery.update_forward_refs()
NormalizationQueryMeta.update_forward_refs()
