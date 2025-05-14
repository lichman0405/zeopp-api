# Probe-Occupiable Volume Request & Response Models
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from pydantic import BaseModel, Field
from typing import Optional


class ProbeVolumeRequest(BaseModel):
    chan_radius: float = Field(..., description="Probe radius used to determine POAV")
    probe_radius: float = Field(..., description="Radius used in MC sampling")
    samples: int = Field(..., description="Number of MC samples per unit cell")
    output_filename: Optional[str] = Field("result.volpo", description="Optional output file name")
    ha: Optional[bool] = Field(True, description="Whether to use high accuracy mode (-ha)")


class ProbeVolumeResponse(BaseModel):
    unitcell_volume: float
    density: float
    av: dict
    nav: dict
    cached: bool
