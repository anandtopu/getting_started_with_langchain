"""Safe command-line failures: never print provider exception bodies or credentials."""

import sys
from collections.abc import Callable

from rich.console import Console

from common.config import ConfigurationError, get_settings
from common.testing import offline_environment


def run_cli(main: Callable[[], None]) -> None:
    """Keep exceptions debuggable in tests while presenting safe CLI diagnostics."""
    try:
        if "--offline" in sys.argv or get_settings().course_offline:
            # Offline also disables ambient tracing and accidental direct HTTP requests.
            with offline_environment():
                main()
        else:
            main()
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except Exception as exc:
        if isinstance(exc, ConfigurationError):
            message = str(exc)
        else:
            # Raw SDK errors can contain request headers or unredacted customer text.
            message = f"The operation failed ({type(exc).__name__})."
        Console(stderr=True).print(message, markup=False)
        Console(stderr=True).print(
            "Run: uv run python scripts/check_env.py (or add --offline to check installation).",
            markup=False,
        )
        raise SystemExit(1) from None
