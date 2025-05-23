# Blocking Spheres API Endpoint
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-22

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path

from app.core.runner import ZeoRunner
from app.models.blocking_spheres import BlockingSpheresResponse
from app.utils.file import save_uploaded_file
from app.utils.parser import parse_block_from_text

router = APIRouter()
runner = ZeoRunner()


@router.post("/api/blocking_spheres", response_model=BlockingSpheresResponse)
async def compute_blocking_spheres(
    structure_file: UploadFile = File(...),
    probe_radius: float = Form(...),
    samples: int = Form(...),
    output_filename: str = Form("result.block"),
    ha: bool = Form(True)
):
    """
    Identify blocking spheres for adsorption using Zeo++ -block
    """
    input_path: Path = save_uploaded_file(structure_file, prefix="block")

    args = []
    if ha:
        args.append("-ha")
    args += ["-block", str(probe_radius), str(samples), input_path.name]

    result = runner.run_command(
        structure_file=input_path,
        zeo_args=args,
        output_files=[output_filename],
        extra_identifier="blocking_spheres"
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

    output_text = result["output_data"].get(output_filename)
    if not output_text:
        raise HTTPException(
            status_code=500,
            detail=f"Output file '{output_filename}' was not generated by Zeo++"
        )

    parsed = parse_block_from_text(output_text)

    return BlockingSpheresResponse(
        **parsed,
        cached=result["cached"]
    )
