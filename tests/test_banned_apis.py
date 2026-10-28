"""Ensure safety/coverage checks catch regressions rather than merely reporting success."""

from scripts.check_legacy import check_source, scan


def test_no_banned_apis():
    assert scan() == []


def test_scanner_rejects_old_factory_and_methods():
    assert check_source("from langgraph.prebuilt import create_" + "react_agent", python=True)
    assert check_source("chain." + "r" + "un('question')", python=True)
    assert check_source("chain." + "pre" + "dict(text='question')", python=True)
    assert check_source("from langchain.memory import Something", python=True)


def test_scanner_allows_standard_library_execution():
    assert check_source("import asyncio\nasyncio." + "r" + "un(main())", python=True) == []
    assert check_source("import subprocess as sp\nsp." + "r" + "un(['python'])", python=True) == []


def test_current_streamlit_runner_is_distinct_from_legacy_model_invocation():
    source = "from streamlit.testing.v1 import AppTest\nAppTest." + "run(app)"
    assert not check_source(source, python=True)
    assert check_source("model." + "run(prompt)", python=True)
