"""Opt-in smoke test; never claims a credential was validated during offline CI."""

import pytest

from common.config import get_settings
from common.models import get_chat_model
from common.tracing import tracing_scope


@pytest.mark.live
def test_selected_live_model():
    settings = get_settings()
    settings.course_offline = False
    with tracing_scope(settings):
        result = get_chat_model(settings=settings).invoke(
            "Reply with a short greeting for Brightwave Outfitters."
        )
    assert result.content
