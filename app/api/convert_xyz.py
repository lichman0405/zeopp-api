# Convert to XYZ Format API Endpoint
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path

from app.core.runner import ZeoRunner
from app.models.convert_xyz import ConvertXYZResponse
from app.utils.file import save_uploaded_file

router = APIRouter()
runner = ZeoRunner()

@router.post("/api/convert_xyz", response_model=ConvertXYZResponse)
async def convert_to_xyz(
    structure_file: UploadFile = File(...),
    output_filename: str = Form("result.xyz")
):
    """
    Convert structure file to XYZ format using Zeo++ -xyz
    """
    input_path: Path = save_uploaded_file(structure_file, prefix="xyz")

    args = ["-xyz", input_path.name]

    result = runner.run_command(
        structure_file=input_path,
        zeo_args=args,
        output_files=[output_filename],
        extra_identifier="convert_xyz"
    )

    if not result["success"]:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Zeo++ failed", "stderr": result["stderr"]}
        )

    output_path = input_path.parent / output_filename
    content = output_path.read_text()

    return ConvertXYZResponse(
        content=content,
        cached=result["cached"]
    )
