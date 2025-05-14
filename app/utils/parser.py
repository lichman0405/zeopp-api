# Zeo++ Output Parser
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-13

import re
from pathlib import Path
from typing import Dict, Any


def parse_res(file_path: Path) -> Dict[str, float]:
    """
    Parse Zeo++ .res file which contains pore diameters

    Format:
        <filename> <included_diameter> <free_diameter> <included_along_free>

    Returns:
        Dict[str, float]: Parsed diameters
    """
    line = file_path.read_text().strip()
    parts = line.split()
    return {
        "included_diameter": float(parts[1]),
        "free_diameter": float(parts[2]),
        "included_along_free": float(parts[3])
    }


def parse_sa(file_path: Path) -> Dict[str, Any]:
    """
    Parse Zeo++ .sa file which contains accessible surface area

    Returns:
        Dict[str, Any]: Parsed ASA and NASA data
    """
    content = file_path.read_text()
    lines = content.splitlines()
    result = {}

    for line in lines:
        if "Unitcell_volume" in line:
            match = re.search(r"Unitcell_volume:\s*([\d\.]+)\s+Density:\s*([\d\.]+)", line)
            if match:
                result["unitcell_volume"] = float(match.group(1))
                result["density"] = float(match.group(2))
        elif "ASA_" in line:
            values = list(map(float, re.findall(r"[\d\.]+", line)))
            result["asa"] = {"A2": values[0], "m2/cm3": values[1], "m2/g": values[2]}
        elif "NASA_" in line:
            values = list(map(float, re.findall(r"[\d\.]+", line)))
            result["nasa"] = {"A2": values[0], "m2/cm3": values[1], "m2/g": values[2]}
    return result


def parse_vol(file_path: Path) -> Dict[str, Any]:
    """
    Parse Zeo++ .vol or .volpo file which contains accessible volume

    Returns:
        Dict[str, Any]: Parsed AV or POAV data
    """
    content = file_path.read_text()
    lines = content.splitlines()
    result = {}

    for line in lines:
        if "Unitcell_volume" in line:
            match = re.search(r"Unitcell_volume:\s*([\d\.]+)\s+Density:\s*([\d\.]+)", line)
            if match:
                result["unitcell_volume"] = float(match.group(1))
                result["density"] = float(match.group(2))
        elif "AV_" in line or "POAV_" in line:
            values = list(map(float, re.findall(r"[\d\.]+", line)))
            result["av"] = {"A3": values[0], "volume_fraction": values[1], "cm3/g": values[2]}
        elif "NAV_" in line or "PONAV_" in line:
            values = list(map(float, re.findall(r"[\d\.]+", line)))
            result["nav"] = {"A3": values[0], "volume_fraction": values[1], "cm3/g": values[2]}
    return result


def parse_chan(file_path: Path) -> Dict[str, Any]:
    """
    Parse Zeo++ .chan file which contains channel dimensionality

    Returns:
        Dict[str, Any]: Number of channels and diameters
    """
    lines = file_path.read_text().splitlines()
    result = {}

    match = re.search(r"(\d+) channels identified of dimensionality (\d+)", lines[0])
    if match:
        result["num_channels"] = int(match.group(1))
        result["dimensionality"] = int(match.group(2))

    channels = []
    for line in lines:
        if line.startswith("Channel"):
            parts = line.strip().split()
            channels.append({
                "id": int(parts[1]),
                "included_diameter": float(parts[2]),
                "free_diameter": float(parts[3]),
                "included_along_free": float(parts[4])
            })
    result["channels"] = channels
    return result


def parse_strinfo(file_path: Path) -> Dict[str, Any]:
    """
    Parse Zeo++ .strinfo file which contains framework/molecule info

    Returns:
        Dict[str, Any]: Framework dimensionality and molecule count
    """
    content = file_path.read_text()
    lines = content.splitlines()

    result = {
        "molecules": 0,
        "frameworks": []
    }

    for line in lines:
        if "Molecules identified:" in line:
            result["molecules"] = int(re.search(r"(\d+)", line).group(1))
        if line.startswith("Framework"):
            parts = line.strip().split()
            result["frameworks"].append({
                "id": int(parts[1]),
                "dimensionality": int(parts[-1])
            })
    return result


def parse_oms(file_path: Path) -> Dict[str, int]:
    """
    Parse Zeo++ .oms file which contains Open Metal Sites count

    Returns:
        Dict[str, int]: Number of OMS identified
    """
    content = file_path.read_text()
    match = re.search(r"OMS detected:\s*(\d+)", content)
    return {"oms_count": int(match.group(1)) if match else 0}
