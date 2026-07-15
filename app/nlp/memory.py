import threading
import uuid
from datetime import datetime, timezone
from typing import Optional

from app.nlp.processor import TextProcessor


class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self._sessions: dict[str, list[dict]] = {}
        self._metadata: dict[str, dict] = {}
        self._lock = threading.RLock()
        self._max_messages = max_messages

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        with self._lock:
            self._sessions[session_id] = []
            self._metadata[session_id] = {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        return session_id

    def get_history(self, session_id: str) -> list[dict]:
        with self._lock:
            return list(self._sessions.get(session_id, []))

    def add_message(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
                self._metadata[session_id] = {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            self._sessions[session_id].append({"role": role, "content": content})
            self._sessions[session_id] = TextProcessor.truncate_history(
                self._sessions[session_id],
                self._max_messages,
            )
            self._metadata[session_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

    def clear_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id not in self._sessions:
                return False
            self._sessions[session_id] = []
            self._metadata[session_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
            return True

    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id not in self._sessions:
                return False
            del self._sessions[session_id]
            del self._metadata[session_id]
            return True

    def remove_last_message(self, session_id: str) -> bool:
        with self._lock:
            if session_id not in self._sessions:
                return False
            if not self._sessions[session_id]:
                return False
            self._sessions[session_id].pop()
            self._metadata[session_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
            return True

    def session_exists(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._sessions

    def get_session_count(self) -> int:
        with self._lock:
            return len(self._sessions)
