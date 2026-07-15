from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import router as api_router
from app.config import settings
from app.state import chat_service

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="AI Chatbot",
    description="Responsive conversational AI chatbot with context-aware responses",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(api_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "model": settings.openai_model,
            "configured": chat_service.is_configured(),
        },
    )
