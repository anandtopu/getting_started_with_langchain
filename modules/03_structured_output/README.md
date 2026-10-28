Assistant version 3: Extract ticket fields into CSV and measure labelled-subset accuracy.

# 03 — Structured output

After this module, you can **extract validated ticket records and measure labelled-subset agreement.**

**Time:** 90 minutes (guided first pass). **Level:** Beginner.
**Cost:** Most short hosted examples are below $0.01 each on the configured low-cost model; see each script's explicit call count. The 100-ticket triage run budgets $0.10, and all-review analysis can approach $1. These are estimates, not spending caps. `--offline` is free and scripted; local Ollama has no API fee. No LangSmith account is required.

## Prerequisites

Complete [Prompt templates](../02_prompt_templates/README.md). Run every command below from the repository root after `uv sync --locked`. Read [provider capabilities](../../docs/PROVIDER_CAPABILITIES.md) before switching model features. To use a real configured provider, omit `--offline`; never mistake fixture output for a quality evaluation.

New terms are defined in the [foundation glossary](../../docs/GLOSSARY.md).

## Learning objectives

- Define Pydantic fields, enums, nested records and nullable identifiers.
- Compare Pydantic, TypedDict and JSON Schema return values.
- Choose provider-native or tool-calling extraction deliberately.
- Bound validation repair and distinguish it from transport retry.
- Export predictions and calculate field and exact-match accuracy.

## The big idea

Structured output is a form with rules on its fields. A provider can constrain how the form is filled, and your Python validator checks the returned form. A correctly shaped form can still contain the wrong facts. Keep extraction separate from evaluation: the model sees ticket text, while the scorer sees the hidden answer key afterward.

## How it works

```mermaid
flowchart LR
    A[Brightwave input] --> B[Application instructions and constraints]
    B --> C[Schema and parser]
    C --> D[Inspectable result]
    D --> E[Validation and human review]
```

**Under the hood:** the script loads local synthetic data and settings, invokes the demonstrated API, and exposes its output. A provider adapter is used only when a model call is needed. Offline mode replaces generation with explicit responses while retaining formatting, parsing, dispatch and SQL behavior. It blocks network in the test and smoke harness.

### Pydantic before the first schema

**Pydantic** is a Python validation library. A class inheriting `BaseModel` describes fields and constraints. `model_validate` checks a dictionary, while `model_dump` returns plain data. `Field(pattern=...)` constrains an identifier; an **enum** is a fixed menu of allowed values. A nested model validates a record inside another record. `str | None` means a value can be text or null. In our schema the key is still required; a default of `None` would additionally make the key optional to supply.

`TypedDict` documents dictionary types but does not itself enforce them at runtime. A JSON Schema is a portable dictionary describing types, required keys and constraints. LangChain returns ordinary dictionaries for those schema forms; the example uses `TypeAdapter` to perform explicit local validation. Pydantic output is validated and returned as a model instance.

Provider-native `method="json_schema"` asks the service to constrain output. `method="function_calling"` represents the desired data as tool arguments, without executing a business tool. Both depend on provider and model capabilities. Ollama schema support and tool quality vary with the selected model. The offline adapter deliberately exercises the real LangChain **tool-output parser** for both choices; it does not emulate server-side JSON constraints. Unsupported live capability is a visible error, never an automatic switch to fabricated data.

The repair lesson catches `ValidationError`, reports which fields need repair, and allows only two attempts. Transport retries address transient network failures; schema repair changes the request after an invalid answer. Repeated failures must surface for human review. A parser such as `PydanticOutputParser` works after text generation, useful when an endpoint lacks native schema support. `StrOutputParser` extracts text but validates no business fields.

The triage application sends all 100 ticket texts through the same prompt/schema path, writes only validated fields to CSV, and aligns predictions to the 50 labelled tickets by `ticket_id`. Exact match requires every field correct; per-field accuracy helps locate errors. Unlabelled tickets do not enter the denominator. The offline score describes a narrow scripted fixture, not an LLM benchmark or general classifier. No labels are placed in prompts.

## Key APIs at a glance

| API or concept | Where to inspect it | What to notice |
|---|---|---|
| Introduce Pydantic v2; with_structured_output; enums, nested models, optional fields | [01_pydantic.py](examples/01_pydantic.py) | Input/output types and the `KEY IDEA` comment |
| TypedDict and JSON Schema; with_structured_output | [02_schema_formats.py](examples/02_schema_formats.py) | Input/output types and the `KEY IDEA` comment |
| Provider-native JSON schema versus tool-calling method; capability checks | [03_output_methods.py](examples/03_output_methods.py) | Input/output types and the `KEY IDEA` comment |
| ValidationError; invalid output, bounded repair and retry; deterministic fixtures | [04_validation_retry.py](examples/04_validation_retry.py) | Input/output types and the `KEY IDEA` comment |
| StrOutputParser, PydanticOutputParser; when parsers remain useful | [05_parsers.py](examples/05_parsers.py) | Input/output types and the `KEY IDEA` comment |

## Walkthrough

Open each file, predict its output, run it, then change one input. Commands use explicit fixtures so the first pass needs no keys.

### 1. Pydantic

**Analogy:** A form inside an envelope. **Under the hood:** Pydantic validates category enums, nullable IDs and a nested record after LangChain parses the structured response. Evidence text does not prove correctness by itself.

```mermaid
flowchart LR
    A["Schema"] --> B["Model"] --> C["Parse"] --> D["Nested validation"]
```

```text
uv run python modules/03_structured_output/examples/01_pydantic.py --offline
```

**Expected:** A TriageEnvelope containing shipping, low, positive and identifiers. Read [the source](examples/01_pydantic.py) to connect the visible result to the exact API call. Live wording and usage can differ.

### 2. Schema formats

**Analogy:** Two descriptions of the same form. **Under the hood:** TypedDict and JSON Schema describe dictionary shapes. LangChain returns dictionaries, and TypeAdapter supplies the explicit local validation step.

```mermaid
flowchart LR
    A["Schema description"] --> B["Dictionary"] --> C["Local validation"]
```

```text
uv run python modules/03_structured_output/examples/02_schema_formats.py --offline
```

**Expected:** Two parsed dictionaries; TypeAdapter validates the TypedDict result. Read [the source](examples/02_schema_formats.py) to connect the visible result to the exact API call. Live wording and usage can differ.

### 3. Output methods

**Analogy:** A constrained form versus a work-order form. **Under the hood:** Native JSON constraints act at the provider; tool-calling output uses schema-shaped arguments. Both need capability checks and local verification.

```mermaid
flowchart LR
    A["Choose method"] --> B["Supported model"] --> C["Parse result"]
```

```text
uv run python modules/03_structured_output/examples/03_output_methods.py --offline
```

**Expected:** Both methods parse the same supplied fixture; provider enforcement is not simulated. Read [the source](examples/03_output_methods.py) to connect the visible result to the exact API call. Live wording and usage can differ.

### 4. Validation retry

**Analogy:** Return an incomplete form for correction. **Under the hood:** ValidationError identifies invalid fields. A bounded second request includes correction instructions; repeated invalid output is raised.

```mermaid
flowchart LR
    A["Extract"] --> B["Validate"] --> C["Repair once"] --> D["Result or error"]
```

```text
uv run python modules/03_structured_output/examples/04_validation_retry.py --offline
```

**Expected:** An invalid priority is rejected, then repaired on the second fixture response. Read [the source](examples/04_validation_retry.py) to connect the visible result to the exact API call. Live wording and usage can differ.

### 5. Parsers

**Analogy:** Read a receipt after it is printed. **Under the hood:** StrOutputParser extracts message text. PydanticOutputParser reads generated JSON and validates it after generation, so it may fail.

```mermaid
flowchart LR
    A["Message"] --> B["Text"] --> C["JSON parser"] --> D["Validated data"]
```

```text
uv run python modules/03_structured_output/examples/05_parsers.py --offline
```

**Expected:** A plain string and a validated TicketTriage object. Read [the source](examples/05_parsers.py) to connect the visible result to the exact API call. Live wording and usage can differ.

## Real-world use case

**Extract ticket fields into CSV and measure labelled-subset accuracy.** Run the mini-application against the committed Brightwave dataset:

```text
uv run python modules/03_structured_output/use_case/ticket_triage.py --offline
```

**Sample input:** 100 tickets; 50 include evaluation labels.

**Sample output:** 100 rows -> .runtime/triage.csv; FIXTURE plumbing score ... labelled: 50.

**Business application:** Operations can import the validated fields into a review queue and inspect per-field errors before deciding whether a live model is reliable. Inspect [the application](use_case/ticket_triage.py). Output remains a draft. Fixtures are predetermined and do not establish that a live model will select the same wording or actions.

## Common mistakes

These exception classes and message excerpts were reproduced against the locked installation. The CLI prints a shorter safe hint; direct calls in tests expose the underlying error.

### Unknown category

```text
ValidationError: 1 validation error for TicketTriage
category
  Input should be 'shipping', 'returns', 'warranty', 'product' or 'privacy' [type=enum, input_value='other', input_type=str]
```

**Fix:** Use a defined category enum; do not silently coerce a different category into shipping.

### Invalid priority

```text
ValidationError: 1 validation error for TicketTriage
priority
  Input should be 'low', 'medium' or 'high' [type=literal_error, input_value='urgent', input_type=str]
```

**Fix:** Map urgency to low, medium or high; urgent is source wording, not an allowed output value.

### Malformed order ID

```text
ValidationError: 1 validation error for TicketTriage
order_id
  String should match pattern '^BW\d{4}$' [type=string_pattern_mismatch, input_value='1001', input_type=str]
```

**Fix:** Keep the BW prefix and four digits, or use null when the source contains no ID.

### Non-JSON response

```text
OutputParserException: Invalid json output: not JSON
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE
```

**Fix:** Use schema-aware output or parser format instructions; catch and bound repair attempts.

## Exercises

Starters have working baseline behavior; improve the named function at `YOUR CODE HERE`. Do not inspect the solution until you have tried the target checks.

1. **Practice — Validate the contract.** Return a TicketTriage instance from a dictionary; reject unsupported categories and malformed IDs. [Starter](exercises/01_practice.py) · [Solution](solutions/01_practice.py).

2. **Apply — Measure extraction honestly.** Compute exact-match accuracy on labelled tickets by ticket_id, ignoring unlabelled rows. Return None for no labels. [Starter](exercises/02_apply.py) · [Solution](solutions/02_apply.py).

3. **Stretch — Bound repair attempts.** Validate model dictionaries, retry ValidationError at most twice, then surface the error. Do not retry unrelated exceptions. [Starter](exercises/03_stretch.py) · [Solution](solutions/03_stretch.py).

```text
uv run python modules/03_structured_output/exercises/01_practice.py --offline
uv run pytest modules/03_structured_output/tests/test_exercises.py --exercise-target exercises
uv run pytest modules/03_structured_output/tests
```

The second command intentionally fails until you complete the starters. The last command checks the supplied solutions plus examples and the use case. Both modes are offline. The [notebook](notebook.ipynb) contains the same example source and a use-case launch cell with outputs cleared; change inputs interactively after the first run. Install notebook tools with `uv sync --group authoring`, then `uv run jupyter lab`.

## Quiz


**What does Pydantic validate?**

<details><summary>Answer</summary>

Types and declared constraints; not whether the extracted facts match the source.

</details>

**Does str | None make a field omissible?**

<details><summary>Answer</summary>

Not by itself. The value may be null; a default is needed if the key may be omitted.

</details>

**Does TypedDict validate at runtime?**

<details><summary>Answer</summary>

No. Add explicit validation when consuming dictionary outputs.

</details>

**How does repair differ from a transport retry?**

<details><summary>Answer</summary>

Repair adds feedback about invalid output; transport retry repeats a request after an infrastructure failure.

</details>

**Why exclude unlabelled tickets from accuracy?**

<details><summary>Answer</summary>

There is no known answer to compare them against.

</details>

**Does a perfect fixture score establish model quality?**

<details><summary>Answer</summary>

No. It checks parsing/scoring plumbing for scripted outputs, not model understanding.

</details>

## Key takeaways

- Define Pydantic fields, enums, nested records and nullable identifiers.
- Compare Pydantic, TypedDict and JSON Schema return values.
- Choose provider-native or tool-calling extraction deliberately.
- Bound validation repair and distinguish it from transport retry.
- Export predictions and calculate field and exact-match accuracy.

## Go deeper

- [Model interface guide](https://docs.langchain.com/oss/python/langchain/models)
- [Structured output guide](https://docs.langchain.com/oss/python/langchain/structured-output)
- [Runnable API reference](https://reference.langchain.com/python/langchain_core/runnables/)
- [Current verification and limits](../../docs/VERIFICATION_NOTES.md)

## Next: LCEL and Runnables

Continue to [LCEL and Runnables](../04_lcel_runnables/README.md). Re-run this module's tests if you change its shared helpers.
