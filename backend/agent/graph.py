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
# DATABASE
# ============================================================

DATABASE_URL = (
    "postgresql://agent:agent_password"
    "@localhost:5433/agent_memory"
)


# ============================================================
# ROUTER
# ============================================================

def should_continue(state):

    messages = state["messages"]

    last_message = messages[-1]

    if getattr(
        last_message,
        "tool_calls",
        None,
    ):
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

builder.add_edge(
    START,
    "llm",
)

builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge(
    "tools",
    "llm",
)


# ============================================================
# POSTGRES CONNECTION
# ============================================================

connection_pool = ConnectionPool(
    conninfo=DATABASE_URL,
    max_size=10,
    kwargs={
        "autocommit": True,
        "prepare_threshold": 0,
    },
)


# ============================================================
# CHECKPOINTER
# ============================================================

checkpointer = PostgresSaver(
    connection_pool
)


# ============================================================
# INITIALIZE DATABASE TABLES
# ============================================================

checkpointer.setup()


# ============================================================
# COMPILE GRAPH
# ============================================================

graph = builder.compile(
    checkpointer=checkpointer
)