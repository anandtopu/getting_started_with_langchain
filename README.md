# Getting started with LangChain

A hands-on course for Python learners building the **Brightwave assistant**, an outdoor-gear support application. Learn how to choose between a model call, chain, retrieval system, agent and graph, then test the choice with synthetic business data.

**Course implementation: all 21 modules, five checkpoints and five capstones.** Includes 139 examples, 63 exercises with solutions, 21 notebooks and five printable cheatsheets. See the [completion checklist](docs/DEFINITION_OF_DONE.md) for measured checks and remaining live-provider evidence. The scripted Support Copilot now scores 6/6 complete contracts and passes the offline release gate; live-provider/customer readiness still needs separate validation. Repository publication is not customer deployment readiness.

Start with [setup and orientation](modules/00_setup/README.md), continue through [tools](modules/05_tools/README.md), then build the [Smart Ticket Desk](checkpoints/01_ticket_desk/README.md). Continue through [loaders and splitters](modules/06_loaders_splitters/README.md) to [advanced RAG](modules/09_advanced_rag/README.md), and finish [Handbook Q&A](checkpoints/02_handbook_qa/README.md). Install retrieval dependencies with `uv sync --extra rag`. The [agents tier](modules/10_agents/README.md) continues through memory, middleware and MCP, ending with [Guarded Support](checkpoints/03_guarded_support/README.md); install it with `uv sync --extra agents`. Continue through [LangGraph orchestration](modules/14_langgraph/README.md) to the [Operations Desk](checkpoints/04_operations_desk/README.md); the optional SDK example needs `uv sync --extra deep`. Continue through [apps](modules/18_apps/README.md), [evaluation](modules/19_evaluation/README.md) and [production](modules/20_production/README.md) to [Production Release](checkpoints/05_production_release/README.md), using `uv sync --extra deployment`. Each lesson includes examples, a realistic application, three runnable exercises with solutions, a quiz, tests and a notebook.

```mermaid
flowchart LR
  A[00–05 Foundations] --> B[06–09 RAG]
  B --> C[10–13 Agents]
  C --> D[14–17 LangGraph]
  D --> E[18–20 Production]
  E --> F[Support Copilot capstone]
```

## Five-minute quick start

Know basic Python, terminal commands and git. Install Python 3.12 (recommended; 3.12–3.14 supported) and [uv](https://docs.astral.sh/uv/getting-started/installation/). Clone `https://github.com/anandtopu/getting_started_with_langchain.git` and enter its directory, or open your existing checkout.

```text
git clone https://github.com/anandtopu/getting_started_with_langchain.git
cd getting_started_with_langchain
```

From the repository root, the following commands work in **Windows PowerShell, macOS and Linux**:

```text
uv sync
uv run python scripts/configure.py
uv run python scripts/check_env.py --offline
uv run python scripts/first_call.py --offline
uv run pytest
```

The first-call output is labelled **OFFLINE FIXTURE**, not generated intelligence. Open `.env`, enter `OPENAI_API_KEY`, then run a real call:

```text
uv run python scripts/check_env.py
uv run python scripts/first_call.py
```

The checked low-cost default is in `.env.example`. A short call should cost well below one cent; usage and the current configured cost estimate print after the answer. Estimates are not invoices. The first-call deadline depends on downloads, hardware and provider access; the offline path needs no account after installation.

## Free local models

Install [Ollama](https://ollama.com/download), start it, then download the two profiles:

```text
ollama pull qwen3:4b
ollama pull embeddinggemma
```

Change **one line** in `.env` to `LLM_PROVIDER=ollama`. Keep `LLM_MODEL` and `EMBEDDINGS_MODEL` blank and `EMBEDDINGS_PROVIDER=auto` to select the local profiles automatically. Run the real-call commands above. Initial model downloads need internet and disk space; inference has no API fee. Image lessons later use the separately downloaded `qwen3-vl:4b` model. See [provider capabilities](docs/PROVIDER_CAPABILITIES.md).

## pip and venv fallback

Create a virtual environment with `python -m venv .venv`. Commands below deliberately use its Python directly, so PowerShell execution policy cannot block activation.

Windows PowerShell:

```powershell
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe scripts/configure.py
.venv\Scripts\python.exe scripts/first_call.py --offline
```

macOS/Linux:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python scripts/configure.py
.venv/bin/python scripts/first_call.py --offline
```

Install a tier with `python -m pip install -e ".[rag]"` using the appropriate virtual-environment Python. uv is recommended for the exact locked development environment; pip resolves the compatible ranges.

## Three ways to learn

1. Follow the [learning path](LEARNING_PATH.md) in order and finish each checkpoint.
2. Find a topic through the [feature map](docs/FEATURE_MAP.md).
3. Start a capstone: [DocuMind](capstones/01_documind/README.md), [Support Copilot](capstones/02_support_copilot/README.md), [Insight Analyst](capstones/03_insight_analyst/README.md), [Research Crew](capstones/04_research_crew/README.md) or optional [Personal Ops](capstones/05_personal_ops/README.md). Each includes a starter, reference solution, tests, evaluation set and rubric.

| Tier | Modules | Guided time, including checkpoint |
|---|---|---:|
| Foundations | 00–05 | 10 h |
| Knowledge and retrieval | 06–09 | 10 h |
| Agents | 10–13 | 12 h |
| Orchestration | 14–17 | 12 h |
| Production | 18–20 | 10 h |

Total: about 54 hours including optional Deep Agents; capstones and exhaustive exercise practice take extra time. Schedules and readiness checks are in the learning path.

Printable field notes: [foundations](cheatsheets/tier_1_foundations.md), [RAG](cheatsheets/tier_2_rag.md), [agents](cheatsheets/tier_3_agents.md), [graphs](cheatsheets/tier_4_graphs.md) and [production](cheatsheets/tier_5_production.md). Each includes a one-page PDF.

## Data, cost and safety

Everything in [data/](data/README.md) is synthetic. Read-only seed databases are kept separate from writable runtime copies. Later lessons execute constrained read-only SQL and record synthetic refunds only in runtime copies; they contact no real customers. `.env` and `.runtime/` are ignored. Tracing is off unless explicitly enabled and can upload prompts; only use synthetic data for this course. A poisoned document is deliberately kept outside the normal policy corpus for the security lesson.

## FAQ

**Do tests require keys or network?** No. After dependency installation, tests force fakes and block networking. A fresh `uv sync` requires downloads unless your cache is populated. `pytest --live` is an explicit opt-in for real providers.

**Can I switch providers?** Yes: `openai`, `anthropic`, `google_genai`, `ollama`. All four chat integrations are in the base install. Embeddings can use OpenAI, Gemini or Ollama independently.

**Why no automatic fallback to fake output?** A broken credential should not look like a successful model call. Failures show a setup hint and a nonzero exit code.

**Is the course finished?** All eight implementation phases are complete. [The completion checklist](docs/DEFINITION_OF_DONE.md) records measured verification and the remaining live-provider gaps. The Support Copilot passes its six offline cases; real-model quality and customer deployment remain unverified.

**Where can I troubleshoot?** Start with `uv run python scripts/check_env.py`, then [troubleshooting](docs/TROUBLESHOOTING.md).

## Development

```text
uv sync --group authoring
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/run_all_examples.py
uv run python scripts/check_links.py
uv run python scripts/check_coverage.py --require-complete
```

The authoring group is needed only to regenerate or inspect data/PDFs and notebooks. `uv sync --all-extras --group authoring` installs the full course stack. See [contributing](CONTRIBUTING.md), [conduct](CODE_OF_CONDUCT.md), [changelog](CHANGELOG.md) and the [MIT license](LICENSE).
