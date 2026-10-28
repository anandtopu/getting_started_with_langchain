# Contributing

Help a beginner make one observable improvement at a time. Use synthetic Brightwave data, current official APIs and a small reproducible example. The course is being delivered in phases; check [progress](docs/progress.json) before treating a planned link as a missing implementation.

## Setup and checks

```text
uv sync --all-extras --group authoring
uv run --no-sync pytest
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync python scripts/check_legacy.py
uv run --no-sync python scripts/check_links.py --allow-planned
uv run --no-sync python scripts/check_coverage.py
uv run --no-sync python scripts/run_all_examples.py
uv run --no-sync pre-commit install
```

`--no-sync` preserves the full environment during contributor checks. A plain `uv run` can return the environment to the default dependency selection. Live tests require `uv run --no-sync pytest --live -m live`; they may cost money and are not required for a content-only change. Never claim a live check passed because its fake equivalent passed.

## Lesson changes

Keep one idea per example. Start with a docstring containing concepts, command, expected output and cost. Use type hints, `main()`, a main guard and `common.models`. Explain why a step exists. Include the failure, its exact reproduced error and the correction. Avoid assertions about real model wording; assert facts, valid fields, citations or tool actions.

Update the [feature map](docs/FEATURE_MAP.md) and [inventory](docs/course-plan.json) when adding or moving a feature. Only add a module to `implemented_modules` when its README, examples, use case, exercises, solutions, quiz, notebook and tests are all present. The final release uses `--require-complete` and strict links; phased development may defer only paths explicitly listed in the inventory.

## Data and notebooks

The generator owns the files listed in [the data manifest](data/manifest.json). Edit the generator, regenerate into a temporary output directory, inspect differences and then regenerate the committed data. Use `uv run --group authoring python scripts/build_data.py`. Fixed seeds and dates keep evaluation meaningful. Do not use real names, emails or payments.

Clear notebook outputs with `uv run --group authoring nbstripout path/to/notebook.ipynb`. Each notebook must execute from top to bottom in its documented environment. Tests and smoke runs must select fake models explicitly and must not depend on ambient credentials.

## Reviews and reports

Include the learner-visible problem, final behavior and relevant validation. Report content errors through the content issue form. Remove secrets from logs; for a security issue, use GitHub's private vulnerability reporting if enabled, otherwise contact the repository owner privately before sharing sensitive details. No contact address is invented by this template.

Contributions are under the [MIT license](LICENSE) and subject to the [code of conduct](CODE_OF_CONDUCT.md).
