# prompt-matrix-runner

<p><img src="assets/banner.svg" alt="prompt-matrix-runner banner"></p>

Prompt templates fail quietly when one variable combination was never tried. `prompt-matrix-runner` expands a
JSON manifest into every prompt variant and checks lightweight expectations without calling a model.

## Manifest

```json
{
  "template": "Classify {ticket} for a {customer} customer.",
  "variables": {
    "ticket": ["refund request", "service outage"],
    "customer": ["trial", "enterprise"]
  },
  "expect": [{"contains": "Classify"}, {"missing": "{ticket}"}]
}
```

## Command

```bash
prompt-matrix-runner examples/matrix.json --preview
prompt-matrix-runner examples/matrix.json --json
```

## What it catches

- templates that reference variables not present in the manifest
- rendered prompts that still contain braces
- expected safety or routing phrases missing from variants
- variant counts that are larger than expected before an eval run

## Development notes

No model key, no network, no external runtime. Tests cover expansion, validation, preview rendering, JSON
output, and CLI help.

MIT.
