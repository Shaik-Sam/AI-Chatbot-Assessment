from openai import OpenAI

from app.config import settings
from app.nlp.memory import ConversationMemory
from app.nlp.processor import TextProcessor


class ChatService:
    SYSTEM_PROMPT = (
        "You are a helpful, knowledgeable AI assistant. "
        "Provide clear, accurate, and conversational responses. "
        "Maintain context from the conversation history. "
        "Be concise but thorough. Use markdown formatting when helpful."
    )

    def __init__(self, memory: ConversationMemory):
        self._memory = memory
        self._processor = TextProcessor()
        self._client = None
        if settings.openai_api_key:
            self._client = OpenAI(api_key=settings.openai_api_key)

    def is_configured(self) -> bool:
        return self._client is not None

    def create_session(self) -> str:
        return self._memory.create_session()

    def get_history(self, session_id: str) -> list[dict]:
        return self._memory.get_history(session_id)

    def clear_session(self, session_id: str) -> bool:
        return self._memory.clear_session(session_id)

    def session_exists(self, session_id: str) -> bool:
        return self._memory.session_exists(session_id)

    def get_session_count(self) -> int:
        return self._memory.get_session_count()

    def process_message(self, session_id: str, user_message: str) -> dict:
        is_valid, error = self._processor.validate_input(user_message)
        if not is_valid:
            return {"success": False, "error": error, "reply": None}

        if not self._client:
            return {
                "success": False,
                "error": "OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file.",
                "reply": None,
            }

        cleaned_message = self._processor.normalize(user_message)
        self._memory.add_message(session_id, "user", cleaned_message)

        history = self._memory.get_history(session_id)
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        messages.extend(history)

        try:
            response = self._client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
            )
            assistant_reply = response.choices[0].message.content or ""
            assistant_reply = self._processor.normalize(assistant_reply)
            self._memory.add_message(session_id, "assistant", assistant_reply)

            return {
                "success": True,
                "error": None,
                "reply": assistant_reply,
                "model": settings.openai_model,
                "tokens_used": response.usage.total_tokens if response.usage else None,
            }
        except Exception as exc:
            self._memory.remove_last_message(session_id)
            return {
                "success": False,
                "error": f"AI service error: {str(exc)}",
                "reply": None,
            }
