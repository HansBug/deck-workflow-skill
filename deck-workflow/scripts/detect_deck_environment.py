#!/usr/bin/env python3
"""Inspect the local environment for deck-generation readiness."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys


PY_MODULES = {
    "pptx": "python-pptx",
    "fitz": "PyMuPDF",
    "PIL": "Pillow",
    "pdf2image": "pdf2image",
}

COMMANDS = ["node", "npm", "soffice", "pdftoppm"]
VERSION_ARGS = {
    "pdftoppm": ["-v"],
}


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def command_info(name: str) -> dict[str, str | bool | None]:
    path = shutil.which(name)
    version = None
    if path:
        try:
            version_args = VERSION_ARGS.get(name, ["--version"])
            completed = subprocess.run(
                [name, *version_args],
                check=False,
                capture_output=True,
                text=True,
            )
            version = (completed.stdout or completed.stderr).strip().splitlines()[0] if (completed.stdout or completed.stderr) else None
        except Exception:
            version = None
    return {"available": bool(path), "path": path, "version": version}


def main() -> int:
    python_modules = {
        package: {
            "import_name": import_name,
            "available": has_module(import_name),
        }
        for import_name, package in PY_MODULES.items()
    }
    commands = {name: command_info(name) for name in COMMANDS}

    python_ready = all(info["available"] for info in python_modules.values())
    python_missing_modules = [package for package, info in python_modules.items() if not info["available"]]
    python_venv_available = has_module("venv")
    python_can_be_prepared = bool(sys.executable) and python_venv_available
    js_ready = commands["node"]["available"] and commands["npm"]["available"]
    review_ready = commands["soffice"]["available"] and commands["pdftoppm"]["available"]

    if python_ready or python_can_be_prepared:
        recommended = "python"
    elif js_ready:
        recommended = "javascript"
    else:
        recommended = "other"

    payload = {
        "python_executable": sys.executable,
        "python_modules": python_modules,
        "python_missing_modules": python_missing_modules,
        "python_venv_available": python_venv_available,
        "python_can_be_prepared": python_can_be_prepared,
        "commands": commands,
        "python_ready": python_ready,
        "javascript_ready": bool(js_ready),
        "review_ready": bool(review_ready),
        "recommended_backend": recommended,
        "notes": [
            "Prefer Python first when the repo is Python-friendly or can be prepared with a local virtual environment.",
            "If Python deck libraries are missing, try `python3 -m venv .venv` and install requirements before falling back to JavaScript.",
            "Use JavaScript as fallback only after the Python path is truly not practical for this repo.",
            "Visual review is not complete unless both soffice and pdftoppm are available.",
            "If the official $slides skill is available, use it alongside this workflow.",
        ],
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
