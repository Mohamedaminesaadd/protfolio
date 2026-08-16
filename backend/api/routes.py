"""
API Routes
==========

FastAPI routes for the Personal AI Agent.
"""

from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    ChatRequest,
    ChatResponse,
)

from backend.agent.main import (
    ask_agent,
    get_final_answer,
    print_tool_calls,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["Agent"],
)


# ============================================================
# CHAT
# ============================================================

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):
    """
    Send a message to the LangGraph agent.
    """

    try:

        # ----------------------------------------------------
        # Clean input
        # ----------------------------------------------------

        message = request.message.strip()

        thread_id = (
            request.thread_id.strip()
            if request.thread_id
            else "amine-session-001"
        )

        if not message:

            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty.",
            )

        # ----------------------------------------------------
        # Debug
        # ----------------------------------------------------

        print("\n" + "=" * 80)
        print("API CHAT REQUEST")
        print("=" * 80)

        print(
            f"[Message] {message}"
        )

        print(
            f"[Thread]  {thread_id}"
        )

        # ----------------------------------------------------
        # RUN THE SAME AGENT USED BY main.py
        # ----------------------------------------------------

        result = ask_agent(
            question=message,
            thread_id=thread_id,
        )

        # ----------------------------------------------------
        # DEBUG TOOL CALLS
        # ----------------------------------------------------

        print_tool_calls(result)

        # ----------------------------------------------------
        # GET FINAL ANSWER
        # ----------------------------------------------------

        answer = get_final_answer(
            result
        )

        print("\n" + "=" * 80)
        print("API AGENT RESPONSE")
        print("=" * 80)

        print(answer)

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return ChatResponse(
            answer=answer,
            thread_id=thread_id,
        )

    except HTTPException:
        raise

    except Exception as error:

        print("\n" + "=" * 80)
        print("API ERROR")
        print("=" * 80)

        print(
            f"{type(error).__name__}: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal agent error.",
        )