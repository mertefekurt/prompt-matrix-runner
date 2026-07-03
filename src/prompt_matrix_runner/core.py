from __future__ import annotations

import itertools
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

PLACEHOLDER = re.compile(r"{([a-zA-Z_][a-zA-Z0-9_]*)}")


@dataclass(frozen=True)
class Variant:
    index: int
    values: dict[str, str]
    prompt: str
    passed: bool
    errors: tuple[str, ...]


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def missing_variables(template: str, variables: dict[str, list[str]]) -> set[str]:
    return set(PLACEHOLDER.findall(template)) - set(variables)


def expand_manifest(manifest: dict) -> list[Variant]:
    template = str(manifest["template"])
    variables = {key: [str(item) for item in value] for key, value in manifest.get("variables", {}).items()}
    missing = missing_variables(template, variables)
    if missing:
        raise ValueError(f"missing variables: {', '.join(sorted(missing))}")
    keys = list(variables)
    variants: list[Variant] = []
    for index, values in enumerate(itertools.product(*(variables[key] for key in keys)), start=1):
        mapping = dict(zip(keys, values, strict=True))
        prompt = template.format(**mapping)
        errors = validate_prompt(prompt, manifest.get("expect", []))
        variants.append(Variant(index, mapping, prompt, not errors, tuple(errors)))
    return variants


def validate_prompt(prompt: str, expectations: list[dict]) -> list[str]:
    errors: list[str] = []
    if "{" in prompt or "}" in prompt:
        errors.append("unresolved placeholder")
    for expectation in expectations:
        if "contains" in expectation and str(expectation["contains"]) not in prompt:
            errors.append(f"missing required text: {expectation['contains']}")
        if "missing" in expectation and str(expectation["missing"]) in prompt:
            errors.append(f"forbidden text present: {expectation['missing']}")
    return errors


def render_preview(variants: list[Variant]) -> str:
    lines = []
    for variant in variants:
        marker = "ok" if variant.passed else "fail"
        lines.append(f"[{marker}] variant {variant.index}: {variant.prompt}")
    return "\n".join(lines) + "\n"


def render_json(variants: list[Variant]) -> str:
    return json.dumps([asdict(variant) for variant in variants], indent=2)
