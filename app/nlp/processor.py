import re
import unicodedata
from typing import Optional


class TextProcessor:
    MAX_INPUT_LENGTH = 4000

    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
        normalized = unicodedata.normalize("NFKC", text)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    @staticmethod
    def validate_input(text: str) -> tuple[bool, Optional[str]]:
        cleaned = TextProcessor.normalize(text)
        if not cleaned:
            return False, "Message cannot be empty."
        if len(cleaned) > TextProcessor.MAX_INPUT_LENGTH:
            return False, f"Message exceeds {TextProcessor.MAX_INPUT_LENGTH} characters."
        return True, None

    @staticmethod
    def estimate_tokens(text: str) -> int:
        if not text:
            return 0
        return max(1, len(text) // 4)

    @staticmethod
    def truncate_history(messages: list[dict], max_messages: int) -> list[dict]:
        if len(messages) <= max_messages:
            return messages
        return messages[-max_messages:]
