# Pore Diameter API Endpoint
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path

from app.models.pore_diameter import PoreDiameterRequest, PoreDiameterResponse
from app.core.runner import ZeoRunner
from app.utils.file import save_uploaded_file
from app.utils.parser import parse_res

router = APIRouter()
runner = ZeoRunner()

@router.post("/api/pore_diameter", response_model=PoreDiameterResponse)
async def compute_pore_diameter(
    structure_file: UploadFile = File(...),
    ha: bool = Form(True),
    output_filename: str = Form("result.res")
):
    """
    Compute largest included / free / along-free sphere diameters using Zeo++ -res
    """
    # Step 1: Save structure file
    input_path: Path = save_uploaded_file(structure_file, prefix="pore")

    # Step 2: Construct Zeo++ args
    args = []
    if ha:
        args.append("-ha")
    args += ["-res", output_filename, input_path.name]

    # Step 3: Run Zeo++
    result = runner.run_command(
        structure_file=input_path,
        zeo_args=args,
        output_files=[output_filename],
        extra_identifier="pore_diameter"
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

    # Step 4: Parse result file
    output_path = input_path.parent / output_filename
    parsed = parse_res(output_path)

    return PoreDiameterResponse(
        **parsed,
        cached=result["cached"]
    )
