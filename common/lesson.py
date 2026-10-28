"""Small command-line conveniences shared by the foundation lessons."""

import argparse

from common.config import Settings, get_settings
from common.pretty import print_text


def lesson_settings() -> Settings:
    """Select an explicit offline fixture without changing the learner's .env."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offline", action="store_true", help="Use scripted fixtures, no API calls"
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    if settings.course_offline:
        print_text("OFFLINE FIXTURE: tests program behavior, not model quality.")
    return settings
