# Open Metal Site Detection API Endpoint
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path

from app.core.runner import ZeoRunner
from app.models.oms_detection import OMSDetectionResponse
from app.utils.file import save_uploaded_file
from app.utils.parser import parse_oms

router = APIRouter()
runner = ZeoRunner()

@router.post("/api/oms_detection", response_model=OMSDetectionResponse)
async def detect_open_metal_sites(
    structure_file: UploadFile = File(...),
    output_filename: str = Form("result.oms")
):
    """
    Detect open metal sites in MOF structure using Zeo++ -oms
    """
    input_path: Path = save_uploaded_file(structure_file, prefix="oms")

    args = ["-oms", input_path.name]

    result = runner.run_command(
        structure_file=input_path,
        zeo_args=args,
        output_files=[output_filename],
        extra_identifier="oms_detection"
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
    parsed = parse_oms(output_path)

    return OMSDetectionResponse(
        **parsed,
        cached=result["cached"]
    )
