"""Reject obsolete teaching patterns, without banning unrelated standard-library methods."""

import ast
import json
import re
from pathlib import Path

from common.config import ROOT

IGNORED_PARTS = {".git", ".venv", ".runtime", "tmp", "__pycache__", ".pytest_cache", ".ruff_cache"}
# Split spellings so the scanner does not exempt its own file or hide forbidden teaching code.
BANNED = [
    "LLM" + "Chain",
    "Conversation" + "Chain",
    "Sequential" + "Chain",
    "Retrieval" + "QA",
    "initialize_" + "agent",
    "Agent" + "Executor",
    "ConversationBuffer" + "Memory",
    "ConversationBufferWindow" + "Memory",
    "ConversationSummary" + "Memory",
    "ConversationSummaryBuffer" + "Memory",
    "ConversationTokenBuffer" + "Memory",
    "langgraph.prebuilt." + "create_react_agent",
    "from langchain." + "llms import",
    "from langchain.chat_models import " + "ChatOpenAI",
]


def source_files(root: Path) -> list[Path]:
    found = []
    for directory, folders, files in root.walk():
        folders[:] = [name for name in folders if name not in IGNORED_PARTS]
        found.extend(
            directory / name for name in files if Path(name).suffix in {".py", ".md", ".ipynb"}
        )
    return found


def check_source(text: str, *, python: bool) -> list[str]:
    findings = [f"Forbidden pattern: {name}" for name in BANNED if name in text]
    if python:
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return findings + ["Invalid Python syntax"]
        standard = {"asyncio", "subprocess"}
        ui_test_classes = {
            alias.asname or alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "streamlit.testing.v1"
            for alias in node.names
            if alias.name == "AppTest"
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                standard.update(a.asname or a.name for a in node.names if a.name in standard)
            if isinstance(node, ast.ImportFrom):
                if node.module == "langgraph.prebuilt" and any(
                    alias.name == "create_" + "react_agent" for alias in node.names
                ):
                    findings.append("Forbidden prebuilt agent factory import")
                if node.module == "langchain.memory" or (
                    node.module and node.module.startswith("langchain_classic")
                ):
                    findings.append("Legacy memory import")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                name = node.func.attr
                owner = node.func.value
                if name in {"r" + "un", "pre" + "dict"} and not (
                    isinstance(owner, ast.Name)
                    and (owner.id in standard or (name == "run" and owner.id in ui_test_classes))
                ):
                    findings.append(f"Legacy invocation on line {node.lineno}")
    else:
        # Markdown snippets are teaching code too; permit standard-library event-loop examples.
        if re.search(r"(?<!asyncio)(?<!subprocess)\.(?:r" + r"un|pre" + r"dict)\(", text):
            findings.append("Legacy invocation in prose/code fence")
    return findings


def scan(root: Path = ROOT) -> list[str]:
    failures = []
    for path in source_files(root):
        if path.relative_to(root).as_posix() == "docs/MIGRATING_FROM_LEGACY.md":
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".ipynb":
            for cell in json.loads(text).get("cells", []):
                failures.extend(
                    f"{path}: {issue}"
                    for issue in check_source(
                        "".join(cell.get("source", [])), python=cell.get("cell_type") == "code"
                    )
                )
        else:
            failures.extend(
                f"{path}: {issue}" for issue in check_source(text, python=path.suffix == ".py")
            )
    return failures


def main() -> None:
    failures = scan()
    for failure in failures:
        print(failure)
    print(f"Legacy API check: {len(failures)} violation(s).")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
