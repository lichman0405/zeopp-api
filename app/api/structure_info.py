# Structure Info API Endpoint
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path

from app.core.runner import ZeoRunner
from app.models.structure_info import StructureInfoResponse
from app.utils.file import save_uploaded_file
from app.utils.parser import parse_strinfo

router = APIRouter()
runner = ZeoRunner()

@router.post("/api/structure_info", response_model=StructureInfoResponse)
async def analyze_structure_info(
    structure_file: UploadFile = File(...),
    output_filename: str = Form("result.strinfo")
):
    """
    Analyze molecular structure and framework info using Zeo++ -strinfo
    """
    input_path: Path = save_uploaded_file(structure_file, prefix="strinfo")

    args = ["-strinfo", input_path.name]

    result = runner.run_command(
        structure_file=input_path,
        zeo_args=args,
        output_files=[output_filename],
        extra_identifier="structure_info"
    )

    if not result["success"]:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Zeo++ failed",
                "stderr": result["stderr"]
            }
        )

    output_path = input_path.parent / output_filename
    parsed = parse_strinfo(output_path)

    return StructureInfoResponse(
        **parsed,
        cached=result["cached"]
    )
