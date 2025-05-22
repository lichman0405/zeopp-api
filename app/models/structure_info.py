# Structure Info Request & Response Models
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from pydantic import BaseModel, Field
from typing import Optional, List


class StructureInfoRequest(BaseModel):
    output_filename: Optional[str] = Field("result.strinfo", description="Optional output file name")


class FrameworkEntry(BaseModel):
    id: int
    dimensionality: int


class StructureInfoResponse(BaseModel):
    num_frameworks: int
    frameworks: List[dict]  # Each dict has id + dimensionality
    cached: bool

