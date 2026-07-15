from app.config import settings
from app.nlp.memory import ConversationMemory
from app.services.chat_service import ChatService

memory = ConversationMemory(max_messages=settings.max_history_messages)
chat_service = ChatService(memory=memory)
