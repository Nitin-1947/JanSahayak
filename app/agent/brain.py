import requests

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.agent.prompts import SYSTEM_PROMPT
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaBrain:

    def __init__(
        self,
        model: str = OLLAMA_MODEL
    ):
        self.model = model
        self.url = (
            f"{OLLAMA_BASE_URL}/api/chat"
        )

    def generate(
        self,
        messages: list[dict],
        system_prompt: str = SYSTEM_PROMPT
    ) -> str:

        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                *messages
            ]
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            return (
                data
                .get("message", {})
                .get("content", "")
                .strip()
            )

        except requests.RequestException as exc:
            logger.error(
                "Ollama request failed: %s",
                exc
            )

            return (
                "माफ कीजिए, अभी AI सेवा से "
                "उत्तर प्राप्त नहीं हो पाया।"
            )