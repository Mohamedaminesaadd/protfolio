"""
Agent Nodes
===========

LLM and tool nodes for the Personal AI Agent.

Architecture:

User
 ↓
LLM
 ↓
Tool Call
 ↓
ToolNode
 ↓
LLM
 ↓
Final Answer
"""

from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode

from backend.agent.prompts import SYSTEM_PROMPT

from backend.tools.rag_tool import search_profile
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.tools.github_tool import (
    search_github_repositories,
    find_my_github_project,
    get_github_repository,
    get_github_readme,
    get_github_file,
)


# ============================================================
# LLM
# ============================================================

llm = ChatOllama(
    model="qwen2.5:14b",
    base_url="http://localhost:11434",
    temperature=0.2,
)


# ============================================================
# TOOLS
# ============================================================

tools = [
    search_profile,

    search_github_repositories,
    find_my_github_project,
    get_github_repository,
    get_github_readme,
    get_github_file,
]


# ============================================================
# NORMAL LLM
# ============================================================

llm_with_tools = llm.bind_tools(
    tools,
    tool_choice="auto",
)


# ============================================================
# PERSONAL PROFILE LLM
# ============================================================

"""
For questions about Mohamed Amine Saad, we want to guarantee that
the model retrieves information from the personal knowledge base.

This prevents Qwen from simply answering from its pretrained
knowledge.
"""

profile_llm = llm.bind_tools(
    [search_profile],
    tool_choice="required",
)


# ============================================================
# DETECT PERSONAL QUESTION
# ============================================================

def is_personal_question(message: str) -> bool:
    """
    Determine whether the user is asking about Mohamed Amine Saad.
    """

    text = message.lower().strip()

    personal_keywords = [
        "mohamed amine saad",
        "amine saad",
        "mohamed",
        "his skills",
        "his skill",
        "his experience",
        "his education",
        "his projects",
        "his technologies",
        "his github",
        "his background",
        "his profile",
        "tell me about amine",
        "tell me about mohamed",
        "about amine",
        "about mohamed",
    ]

    return any(
        keyword in text
        for keyword in personal_keywords
    )


# ============================================================
# LLM NODE
# ============================================================

def llm_node(state):
    """
    Main LangGraph LLM node.

    First request:
        Personal question → force search_profile

    After tool result:
        Use normal LLM to generate final answer.
    """

    messages = state["messages"]

    if not messages:
        return {
            "messages": []
        }


    # --------------------------------------------------------
    # Check the last message
    # --------------------------------------------------------

    last_message = messages[-1]


    # --------------------------------------------------------
    # If we already received a tool result,
    # allow the LLM to generate the final answer normally.
    # --------------------------------------------------------

    message_type = getattr(
        last_message,
        "type",
        None,
    )

    if message_type == "tool":

        print(
            "\n[LLM] Tool result received."
        )

        print(
            "[LLM] Generating final answer..."
        )

        response = llm_with_tools.invoke(
            [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *messages,
            ]
        )

        return {
            "messages": [response]
        }


    # --------------------------------------------------------
    # Extract user message
    # --------------------------------------------------------

    user_message = getattr(
        last_message,
        "content",
        "",
    )

    if not isinstance(
        user_message,
        str,
    ):

        user_message = str(
            user_message
        )


    # ========================================================
    # PERSONAL QUESTION
    # ========================================================

    if is_personal_question(
        user_message
    ):

        print(
            "\n[LLM] Personal question detected."
        )

        print(
            "[LLM] search_profile is REQUIRED."
        )


        response = profile_llm.invoke(
            [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *messages,
            ]
        )

        return {
            "messages": [response]
        }


    # ========================================================
    # GENERAL QUESTION
    # ========================================================

    print(
        "\n[LLM] General question."
    )

    response = llm_with_tools.invoke(
        [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *messages,
        ]
    )

    return {
        "messages": [response]
    }


# ============================================================
# TOOL NODE
# ============================================================

tool_node = ToolNode(
    tools
)