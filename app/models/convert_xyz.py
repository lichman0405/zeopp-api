# XYZ Conversion Request & Response Models
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from pydantic import BaseModel, Field
from typing import Optional


class ConvertXYZRequest(BaseModel):
    output_filename: Optional[str] = Field("result.xyz", description="Optional output file name")


class ConvertXYZResponse(BaseModel):
    content: str
    cached: bool
