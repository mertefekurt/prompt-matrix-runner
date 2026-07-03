from __future__ import annotations

import json

import pytest

from prompt_matrix_runner.cli import main
from prompt_matrix_runner.core import expand_manifest, missing_variables, render_json, render_preview

MANIFEST = {"template": "Hello {name} in {mode}", "variables": {"name": ["A", "B"], "mode": ["fast"]}}


def test_expands_cartesian_product() -> None:
    assert len(expand_manifest(MANIFEST)) == 2


def test_missing_variables_detected() -> None:
    assert missing_variables("{x} {y}", {"x": ["1"]}) == {"y"}


def test_missing_variables_raise() -> None:
    with pytest.raises(ValueError):
        expand_manifest({"template": "{x}", "variables": {}})


def test_preview_marks_ok() -> None:
    assert "[ok]" in render_preview(expand_manifest(MANIFEST))


def test_json_render_has_prompt() -> None:
    assert json.loads(render_json(expand_manifest(MANIFEST)))[0]["prompt"].startswith("Hello")


def test_cli_help(capsys) -> None:
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0
    assert "prompt" in capsys.readouterr().out.lower()
