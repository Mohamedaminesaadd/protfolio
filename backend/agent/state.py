from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared state of the personal AI agent.

    messages:
        Conversation history and tool messages.
    """

    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]