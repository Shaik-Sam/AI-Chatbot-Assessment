from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1, max_length=4000)


class SessionResponse(BaseModel):
    session_id: str
    configured: bool


class ChatResponse(BaseModel):
    success: bool
    reply: str | None = None
    error: str | None = None
    model: str | None = None
    tokens_used: int | None = None


class HistoryResponse(BaseModel):
    session_id: str
    messages: list[dict]


class StatusResponse(BaseModel):
    status: str
    configured: bool
    model: str
    active_sessions: int


def get_chat_service():
    from app.state import chat_service
    return chat_service


@router.get("/health", response_model=StatusResponse)
async def health_check():
    from app.config import settings
    service = get_chat_service()
    return StatusResponse(
        status="healthy",
        configured=service.is_configured(),
        model=settings.openai_model,
        active_sessions=service.get_session_count(),
    )


@router.post("/session", response_model=SessionResponse)
async def create_session():
    service = get_chat_service()
    session_id = service.create_session()
    return SessionResponse(session_id=session_id, configured=service.is_configured())


@router.post("/chat", response_model=ChatResponse)
async def send_message(payload: ChatRequest):
    service = get_chat_service()
    if not service.session_exists(payload.session_id):
        raise HTTPException(status_code=404, detail="Session not found. Create a new session.")
    result = service.process_message(payload.session_id, payload.message)
    return ChatResponse(**result)


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    service = get_chat_service()
    if not service.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found.")
    messages = service.get_history(session_id)
    return HistoryResponse(session_id=session_id, messages=messages)


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    service = get_chat_service()
    if not service.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found.")
    service.clear_session(session_id)
    return {"success": True, "message": "Conversation cleared."}
