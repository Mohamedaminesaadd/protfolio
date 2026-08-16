"""
API Schemas
===========

Request and response models for the Personal AI Agent API.
"""

from pydantic import BaseModel, Field


# ============================================================
# CHAT REQUEST
# ============================================================

class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        description="User message",
    )

    thread_id: str = Field(
        default="amine-session-001",
        min_length=1,
        description="Conversation thread ID",
    )


# ============================================================
# CHAT RESPONSE
# ============================================================

class ChatResponse(BaseModel):

    answer: str

    thread_id: str