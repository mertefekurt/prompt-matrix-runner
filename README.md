# Prompt Matrix Runner

Expand prompt templates into a deterministic test matrix.

![Prompt Matrix Runner cover](assets/readme-cover.svg)

## Manifest shape

The example combines a template, variable lists, and expectation checks. The runner expands every combination and reports whether each variant still matches the expectations.

```bash
git clone https://github.com/mertefekurt/prompt-matrix-runner.git
cd prompt-matrix-runner
python -m pip install -e ".[dev]"
prompt-matrix-runner examples/matrix.json --preview
prompt-matrix-runner examples/matrix.json --json
```
