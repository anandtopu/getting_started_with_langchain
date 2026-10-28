"""Offline is mandatory unless an individual live test is explicitly opted in."""

import pytest

from common.testing import offline_environment


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--exercise-target",
        choices=["solutions", "exercises"],
        default="solutions",
        help="Choose completed solutions or learner-edited starter targets.",
    )
    parser.addoption(
        "--live", action="store_true", default=False, help="Allow marked real-provider tests."
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if not config.getoption("--live"):
        for item in items:
            if item.get_closest_marker("live"):
                item.add_marker(
                    pytest.mark.skip(reason="Real model calls require explicit --live.")
                )


@pytest.fixture(autouse=True)
def prevent_network(request: pytest.FixtureRequest):
    if request.node.get_closest_marker("live") and request.config.getoption("--live"):
        yield
    else:
        with offline_environment():
            yield
