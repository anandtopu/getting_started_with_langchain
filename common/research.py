"""Allowlisted virtual documents and bounded research; no host filesystem tools or shell."""

import re
from pathlib import PurePosixPath

from langchain.tools import tool
from langchain_core.documents import Document

from common.config import Settings
from common.data import data_path
from common.knowledge import identify
from common.retrieval import LexicalRetriever

SOURCES = ("market_brief.md", "customer_trends.md", "product_trends.md")


def virtual_path(path: str, *, writable: bool = False) -> str:
    """Accept one canonical absolute POSIX path; never translate it to a host path."""
    if "\\" in path or "\x00" in path or ":" in path or not path.startswith("/"):
        raise ValueError("Use an absolute virtual POSIX path.")
    parts = PurePosixPath(path).parts
    if ".." in parts or str(PurePosixPath(path)) != path:
        raise ValueError("Virtual paths must be canonical; traversal is forbidden.")
    allowed = {"/sources/" + name for name in SOURCES}
    if path not in ({"/reports/trends.md"} if writable else allowed | {"/reports/trends.md"}):
        raise ValueError("Path is outside the lesson allowlist.")
    return path


class VirtualFiles:
    """Per-run in-memory files. Reports are not persisted unless the host explicitly saves them."""

    def __init__(self) -> None:
        self.files = {
            "/sources/" + name: data_path("research/" + name).read_text(encoding="utf-8")
            for name in SOURCES
        }

    def read(self, path: str) -> str:
        return self.files[virtual_path(path)]

    def write(self, path: str, content: str) -> str:
        key = virtual_path(path, writable=True)
        if len(content) > 12000:
            raise ValueError("Report exceeds the 12,000-character budget.")
        self.files[key] = content
        return key

    def tools(self) -> list:
        @tool
        def read_research(path: str) -> str:
            """Read an allowlisted synthetic research source from the virtual filesystem."""
            return self.read(path)

        @tool
        def write_report(path: str, content: str) -> str:
            """Write only /reports/trends.md in memory; no host disk or shell access."""
            return self.write(path, content)

        return [read_research, write_report]


def research_sources(query: str, settings: Settings, *, web: bool = False) -> list[Document]:
    if web:
        if settings.course_offline:
            raise ValueError("Web search needs an explicit live run.")
        from langchain_tavily import TavilySearch
        from langchain_tavily._utilities import TavilySearchAPIWrapper

        # The wrapper receives the configured secret; neither query nor output includes it.
        client = TavilySearch(
            max_results=3,
            search_depth="basic",
            include_raw_content=False,
            api_wrapper=TavilySearchAPIWrapper(tavily_api_key=settings.tavily_api_key),
        )
        result = client.invoke({"query": query})
        if not isinstance(result, dict) or "results" not in result:
            raise ValueError("Search did not return usable results.")
        return [
            identify(
                Document(
                    page_content=item["content"],
                    metadata={"source": item["url"], "synthetic": False},
                )
            )
            for item in result["results"][:3]
        ]
    docs = [
        identify(
            Document(
                page_content=data_path("research/" + name).read_text(encoding="utf-8"),
                metadata={"source": "data/research/" + name, "synthetic": True},
            )
        )
        for name in SOURCES
    ]
    return LexicalRetriever(docs).search(query)


def validate_report(report: str, files: VirtualFiles) -> list[str]:
    citations = re.findall(r"\[(/sources/[^\]]+)\]", report)
    if not citations or "synthetic" not in report.lower():
        raise ValueError("Label synthetic evidence and include source citations.")
    for citation in citations:
        files.read(citation)
    return sorted(set(citations))
