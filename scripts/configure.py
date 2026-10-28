"""Create .env without replacing existing settings. Run: uv run python scripts/configure.py."""

import shutil
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / ".env"
    try:
        with (root / ".env.example").open("rb") as source, target.open("xb") as output:
            shutil.copyfileobj(source, output)
    except FileExistsError:
        print(".env already exists; your settings were preserved.")
    else:
        print("Created .env. Add a provider key, or set LLM_PROVIDER=ollama for local models.")


if __name__ == "__main__":
    main()
