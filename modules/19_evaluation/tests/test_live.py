"""Selected-provider structured-output test; explicitly skipped without --live."""

import pytest
from pydantic import BaseModel

from common.config import get_settings
from common.models import get_chat_model


class Company(BaseModel):
    company: str


@pytest.mark.live
def test_selected_profile_structured_output():
    settings = get_settings().model_copy(update={"course_offline": False})
    result = (
        get_chat_model(settings=settings)
        .with_structured_output(Company)
        .invoke("The company is Brightwave. Return its name in the requested schema.")
    )
    assert result.company == "Brightwave"
