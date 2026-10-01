import logging

from fastapi import FastAPI, WebSocket
import uvicorn

from app.config import ensure_directories
from app.memory.database import initialize_database
from app.agent.brain import OllamaBrain
from app.schemes.scheme_repository import SchemeRepository
from app.schemes.scheme_matcher import SchemeMatcher
from app.schemes.scheme_service import SchemeService
from app.conversation.manager import ConversationManager
from app.telephony.exotel_voicebot import ExotelVoicebotSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jansahayak-voice-server")

app = FastAPI(title="JanSahayak Voice Server")


def build_manager():
    ensure_directories()
    initialize_database()
    repository = SchemeRepository(__import__("app.config", fromlist=["SCHEMES_DIR"]).SCHEMES_DIR)
    matcher = SchemeMatcher(repository)
    scheme_service = SchemeService(matcher)
    brain = OllamaBrain()
    return ConversationManager(brain, scheme_service)

manager = build_manager()

@app.get("/")
async def health():
    return {"status": "ok", "service": "JanSahayak Voice Server", "websocket": "/voice"}

@app.websocket("/voice")
async def voice_websocket(websocket: WebSocket):
    session = ExotelVoicebotSession(websocket, manager)
    await session.run()


if __name__ == "__main__":
    uvicorn.run("voice_server:app", host="0.0.0.0", port=8000, reload=False)
