"""
Agent Nodes
===========

LLM and tool nodes for the Personal AI Agent.

Architecture:

User
 ↓
Gemini Flash
 ↓
Tool Call
 ↓
ToolNode
 ↓
Gemini Flash
 ↓
Final Answer
"""

# ============================================================
# IMPORTS
# ============================================================

import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode

from backend.agent.prompts import SYSTEM_PROMPT

from backend.tools.rag_tool import search_profile

from backend.tools.github_tool import (
    search_github_repositories,
    find_my_github_project,
    get_github_repository,
    get_github_readme,
    get_github_file,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

LLM_MODEL = "gemini-3-flash-preview"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# ============================================================
# API KEY VALIDATION
# ============================================================

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is not set.\n"
        "Please configure GOOGLE_API_KEY "
        "in the environment variables."
    )


# ============================================================
# LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)


# ============================================================
# TOOLS
# ============================================================

tools = [
    # --------------------------------------------------------
    # Personal knowledge / RAG
    # --------------------------------------------------------

    search_profile,

    # --------------------------------------------------------
    # GitHub
    # --------------------------------------------------------

    search_github_repositories,
    find_my_github_project,
    get_github_repository,
    get_github_readme,
    get_github_file,
]


# ============================================================
# LLM WITH TOOLS
# ============================================================

llm_with_tools = llm.bind_tools(
    tools,
    tool_choice="auto",
)


# ============================================================
# PROFILE LLM
# ============================================================

"""
For personal questions, force the search_profile tool.

This guarantees that personal information comes from
the personal knowledge base instead of the LLM's
pretrained knowledge.
"""

profile_llm = llm.bind_tools(
    [search_profile],
    tool_choice="required",
)


# ============================================================
# PERSONAL QUESTION DETECTION
# ============================================================

def is_personal_question(
    message: str,
) -> bool:
    """
    Determine whether a question is related to
    Mohamed Amine Saad or his portfolio.

    This is a lightweight routing mechanism.
    """

    text = message.lower().strip()

    personal_keywords = [

        # ----------------------------------------------------
        # Person
        # ----------------------------------------------------

        "mohamed amine saad",
        "amine saad",
        "mohamed amine",
        "amine",
        "mohamed",

        # ----------------------------------------------------
        # Personal references
        # ----------------------------------------------------

        "my profile",
        "my skills",
        "my projects",
        "my experience",
        "my education",
        "my technologies",
        "my github",
        "my portfolio",
        "my background",

        "his profile",
        "his skills",
        "his projects",
        "his experience",
        "his education",
        "his technologies",
        "his github",
        "his portfolio",
        "his background",

        # ----------------------------------------------------
        # Portfolio references
        # ----------------------------------------------------

        "my project",
        "this project",
        "that project",

        # ----------------------------------------------------
        # Known projects
        # ----------------------------------------------------

        "hpis",
        "human performance intelligence system",
        "coach ai",
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

    Flow:

        User question
             ↓
        Detect personal question
             ↓
        ┌─────────────────────┐
        │                     │
       YES                    NO
        │                     │
        ▼                     ▼
    search_profile       normal tools
        │                     │
        └──────────┬──────────┘
                   ↓
                ToolNode
                   ↓
              Gemini Flash
                   ↓
              Final answer
    """

    messages = state["messages"]

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not messages:
        return {
            "messages": []
        }

    # ========================================================
    # LAST MESSAGE
    # ========================================================

    last_message = messages[-1]

    message_type = getattr(
        last_message,
        "type",
        None,
    )

    # ========================================================
    # TOOL RESULT
    # ========================================================

    if message_type == "tool":

        print(
            "\n[LLM] Tool result received."
        )

        print(
            f"[LLM] Model: {LLM_MODEL}"
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

    # ========================================================
    # EXTRACT USER MESSAGE
    # ========================================================

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