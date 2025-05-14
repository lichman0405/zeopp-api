# Voronoi Network Export API Endpoint
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path

from app.core.runner import ZeoRunner
from app.models.voronoi_network import VoronoiNetworkResponse
from app.utils.file import save_uploaded_file

router = APIRouter()
runner = ZeoRunner()

@router.post("/api/voronoi_network", response_model=VoronoiNetworkResponse)
async def export_voronoi_network(
    structure_file: UploadFile = File(...),
    use_radii: bool = Form(True),
    output_filename: str = Form("result.nt2")
):
    """
    Export Voronoi network from structure using Zeo++ -nt2
    """
    input_path: Path = save_uploaded_file(structure_file, prefix="nt2")

    args = []
    args.append("-r" if use_radii else "-nor")
    args += ["-nt2", input_path.name]

    result = runner.run_command(
        structure_file=input_path,
        zeo_args=args,
        output_files=[output_filename],
        extra_identifier="voronoi_network"
    )

    if not result["success"]:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Zeo++ failed", "stderr": result["stderr"]}
        )

    output_path = input_path.parent / output_filename
    content = output_path.read_text()

    return VoronoiNetworkResponse(
        content=content,
        cached=result["cached"]
    )
