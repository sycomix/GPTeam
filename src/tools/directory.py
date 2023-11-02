from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..tools.context import ToolContext


def consult_directory(
    tool_context: ToolContext,
    agent_input: str = None,
):
    """Shows a list of all agents and their current locations"""

    # first, craft the event object
    agents = tool_context.context.agents

    return "".join(
        f"{agent['full_name']}\n---------------------\nBio: {agent['public_bio']}\n---------------------\n\n"
        for agent in agents
        if agent["id"] != tool_context.agent_id
    )
