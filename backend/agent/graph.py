import os

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from backend.agent.state import AgentState

from backend.agent.nodes import (
    llm_node,
    tool_node,
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

SUPABASE_DB_URL = os.getenv(
    "SUPABASE_DB_URL"
)

if not SUPABASE_DB_URL:
    raise RuntimeError(
        "SUPABASE_DB_URL environment variable is not configured."
    )


# ============================================================
# ROUTER
# ============================================================

def should_continue(
    state: AgentState,
):
    """
    Decide whether the graph should execute tools
    or finish.

    If the last AI message contains tool calls:
        → ToolNode

    Otherwise:
        → END
    """

    messages = state["messages"]

    if not messages:
        return END

    last_message = messages[-1]

    tool_calls = getattr(
        last_message,
        "tool_calls",
        None,
    )

    if tool_calls:
        return "tools"

    return END


# ============================================================
# BUILD GRAPH
# ============================================================

builder = StateGraph(
    AgentState
)


# ============================================================
# NODES
# ============================================================

builder.add_node(
    "llm",
    llm_node,
)

builder.add_node(
    "tools",
    tool_node,
)


# ============================================================
# EDGES
# ============================================================

# START
#   ↓
# LLM

builder.add_edge(
    START,
    "llm",
)


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

# LLM
#   ↓
# tool calls?
#
# YES → tools
# NO  → END

builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)


# ============================================================
# TOOL → LLM
# ============================================================

builder.add_edge(
    "tools",
    "llm",
)


# ============================================================
# SUPABASE POSTGRES CONNECTION POOL
# ============================================================

connection_pool = ConnectionPool(
    conninfo=SUPABASE_DB_URL,

    max_size=10,

    kwargs={
        "autocommit": True,
        "prepare_threshold": None,
    },
)


# ============================================================
# LANGGRAPH CHECKPOINTER
# ============================================================

checkpointer = PostgresSaver(
    connection_pool
)


# ============================================================
# INITIALIZE CHECKPOINT TABLES
# ============================================================

checkpointer.setup()


# ============================================================
# COMPILE GRAPH
# ============================================================

graph = builder.compile(
    checkpointer=checkpointer,
)
