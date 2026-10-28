# Troubleshooting

Start with `uv run python scripts/check_env.py --offline`. If that succeeds, the Python installation and fake interfaces work. Run it without `--offline` to check selected keys or the local Ollama server. This does not spend tokens validating a hosted key.

| Symptom | Meaning | Fix |
|---|---|---|
| `Set OPENAI_API_KEY in .env for openai.` | The selected hosted provider has no key | Run `scripts/configure.py`, edit `.env`, or select Ollama |
| `Invalid configuration for: MODEL_TIMEOUT.` | A setting cannot be parsed or violates its bounds | Compare `.env.example`; timeout must be positive and at most 300 seconds |
| `Ollama is unavailable; start it and check OLLAMA_BASE_URL.` | No reachable server at the configured endpoint | Start Ollama and rerun the environment check |
| `An Ollama profile is not installed; pull the models in .env.` | Server is up, but a selected model is absent | Pull both the chat and embedding profiles; image models are separate |
| `The operation failed (AuthenticationError).` | The provider rejected credentials | Replace the key in `.env`; do not paste it into an issue |
| `The operation failed (RateLimitError).` | Request rate or account quota was exceeded | Inspect the provider account; reduce concurrency and use bounded retries |
| `Network disabled in offline mode; use an explicit live run.` | An offline code path tried to reach a service | Keep fixtures offline; use `--live` only when intentionally testing a real provider |
| `Writable databases must be outside committed data/.` | A write target could alter the seed corpus | Use `.runtime/orders.db` or a test temporary directory |
| `FileExistsError` when copying orders | A learner database already exists | Choose a new runtime filename; copies intentionally never overwrite |
| `attempt to write a readonly database` | Seed access is intentionally read-only | Create a writable copy for a write lesson |
| `ModuleNotFoundError` for an integration | The dependency extra or editable install is missing | Run `uv sync` with the required extra, from the checkout root |

The CLI intentionally suppresses raw SDK exception bodies because they can contain request data. Unit tests call functions directly so programming errors still show tracebacks. Record the command, package versions and exception class when filing an issue; omit keys and personal information.

## Windows paths and environments

Use the repository-root commands exactly as shown. Python uses `pathlib` for data paths, so spaces in your checkout path work. The pip fallback invokes `.venv\Scripts\python.exe` directly and does not require PowerShell activation. If your user cache is not writable, set `UV_CACHE_DIR` to a writable folder for that terminal session. This is a machine permission issue, not a reason to change provider code.

## Old tutorials and future lessons

Do not copy imports from older framework tutorials without checking the current official reference. Use the model factory and `invoke` interface shown in this checkout. The full old-to-new migration guide, Chroma persistence diagnostics, Jupyter async guidance, tool-schema failures and recursion-limit examples will be added alongside their teaching modules and audited in Phase 8. They are not presented here as tested errors before those implementations exist.
