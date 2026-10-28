"""Cost estimates must not silently apply to another model or expose credentials."""

from common.config import Settings
from common.pretty import estimate_cost, redact


def test_cost_math_and_unknown_cases():
    settings = Settings(
        llm_model="priced-model",
        cost_model="priced-model",
        cost_input_per_million=0.1,
        cost_output_per_million=0.5,
    )
    assert estimate_cost({"input_tokens": 4000, "output_tokens": 1000}, settings) == 0.0009
    assert estimate_cost(None, settings) is None
    settings.llm_model = "different-model"
    assert estimate_cost({"input_tokens": 4000, "output_tokens": 1000}, settings) is None


def test_custom_secrets_are_redacted():
    settings = Settings(openai_api_key="custom-value", postgres_uri="postgres://secret")
    output = redact("custom-value and postgres://secret and sk-123456789012345", settings)
    assert "custom-value" not in output
    assert "postgres://secret" not in output
    assert "sk-123456789012345" not in output
