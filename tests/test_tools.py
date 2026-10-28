"""MCP schemas expose data operations, never the host-only approval method."""

import pytest

pytest.importorskip("fastmcp")
from fastmcp import Client

from common.personal_ops import OpsRepository, ops_server


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["notes", "tasks"])
async def test_official_mcp_discovery_has_no_approval_tool(tmp_path, kind):
    async with Client(ops_server(OpsRepository(tmp_path, "learner"), kind)) as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools}
        assert names == (
            {"notes_list", "notes_create"}
            if kind == "notes"
            else {"tasks_list", "tasks_create", "tasks_complete"}
        )
        assert all("owner" not in tool.input_schema.get("properties", {}) for tool in tools)
        assert not any("approve" in name for name in names)


@pytest.mark.asyncio
async def test_agent_completes_only_preapproved_owned_task(tmp_path):
    from common.config import Settings
    from common.personal_ops import run_ops

    repo = OpsRepository(tmp_path, "learner")
    payload = {"item_id": "existing-task", "title": "Inspect synthetic evidence"}
    repo.apply("tasks_create", payload, repo.approve("tasks_create", payload))
    action = [{"operation": "tasks_complete", "payload": {"item_id": "existing-task"}}]
    denied = await run_ops(tmp_path, Settings(course_offline=True), action)
    assert denied["tasks"][0]["done"] == 0
    accepted = await run_ops(tmp_path, Settings(course_offline=True), action, approved=True)
    assert accepted["tasks"][0]["done"] == 1
    assert accepted["audit"][0]["operation"] == "tasks_complete"
