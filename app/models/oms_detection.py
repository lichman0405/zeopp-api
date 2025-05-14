# Open Metal Site Detection Models
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from pydantic import BaseModel, Field
from typing import Optional


class OMSDetectionRequest(BaseModel):
    output_filename: Optional[str] = Field("result.oms", description="Optional output file name")


class OMSDetectionResponse(BaseModel):
    oms_count: int
    cached: bool
