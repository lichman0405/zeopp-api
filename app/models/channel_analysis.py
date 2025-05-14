# Channel Dimensionality Request & Response Models
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class ChannelAnalysisRequest(BaseModel):
    probe_radius: float = Field(..., description="Radius of spherical probe")
    output_filename: Optional[str] = Field("result.chan", description="Optional output file name")
    ha: Optional[bool] = Field(True, description="Whether to use high accuracy mode (-ha)")


class ChannelEntry(BaseModel):
    id: int
    included_diameter: float
    free_diameter: float
    included_along_free: float


class ChannelAnalysisResponse(BaseModel):
    num_channels: int
    dimensionality: int
    channels: List[ChannelEntry]
    cached: bool
