"""Check local Markdown links offline; external links require an explicit --external run."""

import argparse
import json
import re
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

import httpx

from common.config import ROOT
from scripts.check_legacy import source_files


def markdown_files(root: Path) -> list[Path]:
    return [path for path in source_files(root) if path.suffix == ".md"]


def links(path: Path) -> list[str]:
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    return re.findall(r"\]\(([^\s)]+)\)", text)


def anchors(path: Path) -> set[str]:
    result: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^#{1,6} ", line):
            continue
        label = re.sub(r"^#+\s+", "", line).strip().lower()
        slug = re.sub(r"[^\w\- ]", "", label).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        result.add(slug if number == 0 else f"{slug}-{number}")
    return result


def check_local(root: Path = ROOT, *, allow_planned: bool = False) -> tuple[list[str], int]:
    manifest = root / "docs/course-plan.json"
    planned = (
        set(json.loads(manifest.read_text(encoding="utf-8"))["planned_files"])
        if manifest.exists()
        else set()
    )
    failures = []
    deferred = 0
    for path in markdown_files(root):
        for target in links(path):
            parsed = urlsplit(target)
            if parsed.scheme in {"https", "http", "mailto"}:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not resolved.is_relative_to(root.resolve()):
                failures.append(f"{path.name}: link leaves checkout: {target}")
            elif not resolved.exists():
                relative = resolved.relative_to(root.resolve()).as_posix()
                if allow_planned and relative in planned:
                    deferred += 1
                else:
                    failures.append(f"{path.name}: missing {target}")
            elif (
                parsed.fragment
                and resolved.suffix == ".md"
                and unquote(parsed.fragment) not in anchors(resolved)
            ):
                failures.append(f"{path.name}: missing anchor {target}")
    return failures, deferred


def check_external(root: Path = ROOT) -> list[str]:
    urls = sorted(
        {u for path in markdown_files(root) for u in links(path) if u.startswith("https://")}
    )
    failures = []
    with httpx.Client(
        follow_redirects=True, timeout=20, headers={"User-Agent": "Brightwave-course-link-check"}
    ) as client:
        for url in urls:
            for attempt in range(3):
                try:
                    response = client.get(url)
                    if response.is_success:
                        break
                    if response.status_code not in {429, 500, 502, 503, 504}:
                        failures.append(f"HTTP {response.status_code}: {url}")
                        break
                except httpx.HTTPError:
                    pass
                if attempt == 2:
                    failures.append(f"Unreachable after three attempts: {url}")
                else:
                    time.sleep(attempt + 1)
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-planned", action="store_true", help="Report future course links separately."
    )
    parser.add_argument(
        "--external", action="store_true", help="Also request public external URLs."
    )
    args = parser.parse_args()
    failures, deferred = check_local(allow_planned=args.allow_planned)
    if args.external:
        failures.extend(check_external())
    for failure in failures:
        print(failure)
    print(
        f"Link check: {len(failures)} failure(s), {deferred} explicitly planned link(s) deferred."
    )
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
