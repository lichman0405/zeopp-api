# Surface Area Request & Response Models
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from pydantic import BaseModel, Field
from typing import Optional


class SurfaceAreaRequest(BaseModel):
    chan_radius: float = Field(..., description="Radius used to determine accessibility of void space")
    probe_radius: float = Field(..., description="Radius used in Monte Carlo sampling")
    samples: int = Field(..., description="Number of Monte Carlo samples per atom")
    output_filename: Optional[str] = Field("result.sa", description="Optional output file name")
    ha: Optional[bool] = Field(True, description="Whether to use high accuracy mode (-ha)")


class SurfaceAreaResponse(BaseModel):
    unitcell_volume: float
    density: float
    asa: dict
    nasa: dict
    cached: bool
