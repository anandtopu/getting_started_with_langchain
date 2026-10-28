# Planned final repository tree

Updated in Phase 7; includes future capstones and final-release files. See [progress](progress.json). Credentials, caches and runtime files are excluded.

```text
getting_started_with_langchain/
├── .dockerignore
├── .env.example
├── .gitattributes
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug.yml
│   │   ├── content_error.yml
│   │   └── new_example.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LEARNING_PATH.md
├── LICENSE
├── README.md
├── capstones/
│   ├── 01_documind/
│   │   ├── README.md
│   │   ├── app.py
│   │   ├── eval.jsonl
│   │   ├── evaluation_report.md
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       ├── test_acceptance.py
│   │       └── test_evaluation.py
│   ├── 02_support_copilot/
│   │   ├── .dockerignore
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── api.py
│   │   ├── app.py
│   │   ├── eval.jsonl
│   │   ├── langgraph.json
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       ├── test_acceptance.py
│   │       ├── test_api.py
│   │       └── test_evaluation.py
│   ├── 03_insight_analyst/
│   │   ├── README.md
│   │   ├── eval.jsonl
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       ├── test_acceptance.py
│   │       └── test_evaluation.py
│   ├── 04_research_crew/
│   │   ├── README.md
│   │   ├── eval.jsonl
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       ├── test_acceptance.py
│   │       └── test_evaluation.py
│   └── 05_personal_ops/
│       ├── README.md
│       ├── eval.jsonl
│       ├── notes_server.py
│       ├── rubric.md
│       ├── solution.py
│       ├── starter.py
│       ├── tasks_server.py
│       └── tests/
│           ├── test_acceptance.py
│           └── test_evaluation.py
├── cheatsheets/
│   ├── tier_1_foundations.md
│   ├── tier_2_rag.md
│   ├── tier_3_agents.md
│   ├── tier_4_graphs.md
│   └── tier_5_production.md
├── checkpoints/
│   ├── 01_ticket_desk/
│   │   ├── README.md
│   │   ├── eval.jsonl
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       └── test_acceptance.py
│   ├── 02_handbook_qa/
│   │   ├── README.md
│   │   ├── eval.jsonl
│   │   ├── evaluation_report.json
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       └── test_acceptance.py
│   ├── 03_guarded_support/
│   │   ├── README.md
│   │   ├── eval.jsonl
│   │   ├── evaluation_report.json
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       └── test_acceptance.py
│   ├── 04_operations_desk/
│   │   ├── README.md
│   │   ├── design_rationale.md
│   │   ├── eval.jsonl
│   │   ├── evaluation_report.json
│   │   ├── rubric.md
│   │   ├── solution.py
│   │   ├── starter.py
│   │   └── tests/
│   │       └── test_acceptance.py
│   └── 05_production_release/
│       ├── README.md
│       ├── eval.jsonl
│       ├── evaluation_report.json
│       ├── rubric.md
│       ├── solution.py
│       ├── starter.py
│       └── tests/
│           └── test_acceptance.py
├── common/
│   ├── __init__.py
│   ├── advanced_rag.py
│   ├── agent.py
│   ├── budget.py
│   ├── config.py
│   ├── data.py
│   ├── deployment.py
│   ├── desk.py
│   ├── errors.py
│   ├── evaluation.py
│   ├── experiments.py
│   ├── fixtures.py
│   ├── graphs.py
│   ├── guardrails.py
│   ├── handbook.py
│   ├── knowledge.py
│   ├── lesson.py
│   ├── mcp.py
│   ├── memory.py
│   ├── models.py
│   ├── operations.py
│   ├── pretty.py
│   ├── rag.py
│   ├── release.py
│   ├── research.py
│   ├── resilience.py
│   ├── retrieval.py
│   ├── returns.py
│   ├── schemas.py
│   ├── security.py
│   ├── service.py
│   ├── support_evaluation.py
│   ├── testing.py
│   ├── tools.py
│   ├── tracing.py
│   ├── triage.py
│   ├── ui.py
│   ├── vector_index.py
│   ├── web.py
│   └── workflows.py
├── conftest.py
├── data/
│   ├── README.md
│   ├── eval/
│   │   ├── agent_conversations.jsonl
│   │   ├── rag.jsonl
│   │   └── triage.jsonl
│   ├── faq.json
│   ├── fixtures/
│   │   ├── policy.html
│   │   ├── product.png
│   │   └── product.svg
│   ├── handbook/
│   │   ├── employee_handbook.md
│   │   └── employee_handbook.pdf
│   ├── manifest.json
│   ├── orders.db
│   ├── policies/
│   │   ├── privacy.md
│   │   ├── returns.md
│   │   ├── shipping.md
│   │   └── warranty.md
│   ├── products.csv
│   ├── research/
│   │   ├── customer_trends.md
│   │   ├── market_brief.md
│   │   └── product_trends.md
│   ├── reviews.csv
│   ├── security/
│   │   └── poisoned_doc.md
│   └── support_tickets.jsonl
├── docs/
│   ├── CHOOSING_THE_RIGHT_TOOL.md
│   ├── COMPLETION_CHECKLIST.md
│   ├── FEATURE_MAP.md
│   ├── GLOSSARY.md
│   ├── MENTAL_MODEL.md
│   ├── MIGRATING_FROM_LEGACY.md
│   ├── PHASE_1_PLAN.md
│   ├── PROVIDER_CAPABILITIES.md
│   ├── REPOSITORY_TREE.md
│   ├── TROUBLESHOOTING.md
│   ├── VERIFICATION_NOTES.md
│   ├── course-plan.json
│   ├── dependency-candidates.in
│   ├── dependency-resolution.txt
│   ├── phase3-verification.json
│   ├── phase4-verification.json
│   ├── phase5-verification.json
│   ├── phase6-verification.json
│   ├── phase7-verification.json
│   ├── progress.json
│   ├── pypi-verification-phase2.json
│   └── pypi-verification.json
├── langgraph.json
├── modules/
│   ├── 00_setup/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_llm_basics.py
│   │   │   ├── 02_ecosystem.py
│   │   │   └── 03_verify_environment.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── first_call.py
│   ├── 01_chat_models/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_hello_model.py
│   │   │   ├── 02_message_types.py
│   │   │   ├── 03_streaming.py
│   │   │   ├── 04_batch_async.py
│   │   │   ├── 05_parameters.py
│   │   │   ├── 06_usage_cost.py
│   │   │   ├── 07_multimodal.py
│   │   │   ├── 08_rate_limit.py
│   │   │   └── 09_http_by_hand.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── reply_drafter.py
│   ├── 02_prompt_templates/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_variables.py
│   │   │   ├── 02_chat_history.py
│   │   │   ├── 03_few_shot.py
│   │   │   └── 04_prompt_files.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── prompts/
│   │   │   ├── brand_voice.txt
│   │   │   └── tone_rewrite.txt
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── brand_writer.py
│   ├── 03_structured_output/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_pydantic.py
│   │   │   ├── 02_schema_formats.py
│   │   │   ├── 03_output_methods.py
│   │   │   ├── 04_validation_retry.py
│   │   │   └── 05_parsers.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── ticket_triage.py
│   ├── 04_lcel_runnables/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_sequence.py
│   │   │   ├── 02_parallel.py
│   │   │   ├── 03_passthrough.py
│   │   │   ├── 04_python_functions.py
│   │   │   ├── 05_routing.py
│   │   │   ├── 06_resilience.py
│   │   │   ├── 07_config_batch.py
│   │   │   └── 08_events_diagram.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── review_insights.py
│   ├── 05_tools/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_tool_schema.py
│   │   │   ├── 02_args_schema.py
│   │   │   ├── 03_dispatch.py
│   │   │   ├── 04_parallel_choice.py
│   │   │   ├── 05_manual_agent.py
│   │   │   ├── 06_runtime.py
│   │   │   └── 07_sql_safety.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── order_status.py
│   ├── 06_loaders_splitters/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_documents.py
│   │   │   ├── 02_pdf_lazy.py
│   │   │   ├── 03_file_loaders.py
│   │   │   ├── 04_web_loader.py
│   │   │   ├── 05_recursive_chunks.py
│   │   │   ├── 06_markdown_chunks.py
│   │   │   └── 07_token_code_chunks.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── knowledge_ingest.py
│   ├── 07_embeddings_retrievers/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_cosine_by_hand.py
│   │   │   ├── 02_embedding_interface.py
│   │   │   ├── 03_memory_store.py
│   │   │   ├── 04_persistent_chroma.py
│   │   │   ├── 05_document_lifecycle.py
│   │   │   ├── 06_scores_mmr_filters.py
│   │   │   ├── 07_retriever.py
│   │   │   └── 08_embedding_cache.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── product_search.py
│   ├── 08_rag_fundamentals/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_index_retrieve.py
│   │   │   ├── 02_lcel_rag.py
│   │   │   ├── 03_grounding_citations.py
│   │   │   └── 04_retrieval_tool.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── ask_brightwave.py
│   ├── 09_advanced_rag/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_query_rewrite.py
│   │   │   ├── 02_hybrid.py
│   │   │   ├── 03_rerank_compress.py
│   │   │   ├── 04_parent_retrieval.py
│   │   │   ├── 05_query_filters.py
│   │   │   ├── 06_conversation.py
│   │   │   ├── 07_evaluate.py
│   │   │   └── 08_failure_gallery.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── results/
│   │   │   ├── README.md
│   │   │   └── before_after.json
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── rag_benchmark.py
│   ├── 10_agents/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_create_agent.py
│   │   │   ├── 02_trace_stream.py
│   │   │   ├── 03_response_format.py
│   │   │   ├── 04_context.py
│   │   │   ├── 05_errors_limits.py
│   │   │   └── 06_return_write.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── support_agent.py
│   ├── 11_memory/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_stateless_threads.py
│   │   │   ├── 02_sqlite_checkpoint.py
│   │   │   ├── 03_trim.py
│   │   │   ├── 04_summarize.py
│   │   │   ├── 05_custom_state.py
│   │   │   ├── 06_long_term_store.py
│   │   │   └── 07_durable_preferences.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── remembering_agent.py
│   ├── 12_middleware/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_hooks.py
│   │   │   ├── 02_custom_middleware.py
│   │   │   ├── 03_pii.py
│   │   │   ├── 04_approval.py
│   │   │   ├── 05_fallback.py
│   │   │   ├── 06_call_limits.py
│   │   │   ├── 07_retry.py
│   │   │   ├── 08_tool_selector.py
│   │   │   ├── 09_todo.py
│   │   │   └── 10_dynamic_model.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── guarded_agent.py
│   ├── 13_mcp/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_official_server.py
│   │   │   ├── 02_stdio_client.py
│   │   │   ├── 03_http_client.py
│   │   │   ├── 04_agent_connection.py
│   │   │   └── 05_trust_boundary.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       ├── inventory_agent.py
│   │       └── inventory_server.py
│   ├── 14_langgraph/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_state_graph.py
│   │   │   ├── 02_reducers.py
│   │   │   ├── 03_routing_command.py
│   │   │   ├── 04_manual_agent_graph.py
│   │   │   ├── 05_persistence.py
│   │   │   ├── 06_interrupt.py
│   │   │   ├── 07_time_travel.py
│   │   │   ├── 08_subgraphs.py
│   │   │   ├── 09_stream_modes.py
│   │   │   ├── 10_functional_api.py
│   │   │   └── 11_studio.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── return_workflow.py
│   ├── 15_workflows/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_chain_gate.py
│   │   │   ├── 02_route.py
│   │   │   ├── 03_parallel.py
│   │   │   ├── 04_send_map_reduce.py
│   │   │   ├── 05_orchestrator_workers.py
│   │   │   ├── 06_evaluator_optimizer.py
│   │   │   └── 07_choose_workflow.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── weekly_report.py
│   ├── 16_multi_agent/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_supervisor_tools.py
│   │   │   ├── 02_handoffs.py
│   │   │   ├── 03_router.py
│   │   │   ├── 04_context_boundaries.py
│   │   │   └── 05_compare_single.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── operations_team.py
│   ├── 17_deep_agents/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_plan_by_hand.py
│   │   │   ├── 02_virtual_files.py
│   │   │   ├── 03_subagents.py
│   │   │   ├── 04_deepagents_sdk.py
│   │   │   └── 05_search_sources.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       └── research_report.py
│   ├── 18_apps/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_async_basics.py
│   │   │   ├── 02_sse.py
│   │   │   ├── 03_streamlit_chat.py
│   │   │   ├── 04_approval_ui.py
│   │   │   └── 05_session_isolation.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       ├── api.py
│   │       ├── app.py
│   │       └── support_web.py
│   ├── 19_evaluation/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_trace.py
│   │   │   ├── 02_fake_models.py
│   │   │   ├── 03_live_tests.py
│   │   │   ├── 04_datasets_evaluate.py
│   │   │   ├── 05_trajectory.py
│   │   │   ├── 06_prompt_regression.py
│   │   │   └── 07_local_harness.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── prompts/
│   │   │   ├── support_v1.txt
│   │   │   └── support_v2.txt
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   ├── test_live.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       ├── eval.jsonl
│   │       ├── evaluation_report.json
│   │       └── support_eval.py
│   ├── 20_production/
│   │   ├── README.md
│   │   ├── examples/
│   │   │   ├── 01_config_resilience.py
│   │   │   ├── 02_cache_budget.py
│   │   │   ├── 03_structured_logging.py
│   │   │   ├── 04_injection.py
│   │   │   ├── 05_least_privilege.py
│   │   │   ├── 06_docker.py
│   │   │   ├── 07_agent_server.py
│   │   │   └── 08_postgres.py
│   │   ├── exercises/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── notebook.ipynb
│   │   ├── quiz.md
│   │   ├── solutions/
│   │   │   ├── 01_practice.py
│   │   │   ├── 02_apply.py
│   │   │   └── 03_stretch.py
│   │   ├── tests/
│   │   │   ├── test_examples.py
│   │   │   ├── test_exercises.py
│   │   │   └── test_use_case.py
│   │   └── use_case/
│   │       ├── .dockerignore
│   │       ├── Dockerfile
│   │       ├── Dockerfile.dockerignore
│   │       ├── langgraph.json
│   │       └── production_assistant.py
│   └── conftest.py
├── pyproject.toml
├── scripts/
│   ├── __init__.py
│   ├── _smoke_worker.py
│   ├── build_data.py
│   ├── check_coverage.py
│   ├── check_env.py
│   ├── check_legacy.py
│   ├── check_links.py
│   ├── check_notebooks.py
│   ├── configure.py
│   ├── evaluate.py
│   ├── first_call.py
│   └── run_all_examples.py
├── tests/
│   ├── conftest.py
│   ├── test_agent_contracts.py
│   ├── test_banned_apis.py
│   ├── test_budget.py
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_course_structure.py
│   ├── test_data.py
│   ├── test_evaluation.py
│   ├── test_evaluation_contracts.py
│   ├── test_examples.py
│   ├── test_foundation_contracts.py
│   ├── test_links.py
│   ├── test_live.py
│   ├── test_models.py
│   ├── test_notebooks.py
│   ├── test_orchestration_contracts.py
│   ├── test_pretty.py
│   ├── test_production_contracts.py
│   ├── test_rag_contracts.py
│   ├── test_security.py
│   ├── test_tools.py
│   └── test_web_contracts.py
└── uv.lock
```
