from __future__ import annotations

import argparse
from pathlib import Path

from prompt_matrix_runner.core import expand_manifest, load_manifest, render_json, render_preview


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Expand and validate prompt test matrices.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--preview", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    variants = expand_manifest(load_manifest(args.manifest))
    print(render_json(variants) if args.json else render_preview(variants), end="")
    return 0 if all(variant.passed for variant in variants) else 1
