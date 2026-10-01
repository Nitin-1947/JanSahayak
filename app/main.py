from app.config import (
    ensure_directories,
    SCHEMES_DIR,
    KNOWLEDGE_DIR
)

from app.memory.database import (
    initialize_database
)

from app.agent.brain import OllamaBrain

from app.schemes.scheme_repository import (
    SchemeRepository
)

from app.schemes.scheme_matcher import (
    SchemeMatcher
)

from app.schemes.scheme_service import (
    SchemeService
)

from app.conversation.manager import (
    ConversationManager
)


def main():

    print(
        "\n======================================"
    )

    print(
        " Hindi Government AI Assistant"
    )

    print(
        "======================================\n"
    )

    ensure_directories()

    initialize_database()

    repository = SchemeRepository(
        SCHEMES_DIR
    )

    matcher = SchemeMatcher(
        repository
    )

    scheme_service = SchemeService(
        matcher
    )

    brain = OllamaBrain()

    manager = ConversationManager(
        brain,
        scheme_service
    )

    user_id = manager.create_user()

    print(
        "AI: नमस्ते! मैं आपकी सरकारी योजनाओं "
        "और सामान्य नागरिक सेवाओं से जुड़ी "
        "जानकारी में सहायता कर सकता हूँ।"
    )

    print(
        "AI: आप Hindi या Hinglish में बात कर सकते हैं।"
    )

    print(
        "\nType 'exit' to stop.\n"
    )

    while True:

        user_input = input(
            "आप: "
        ).strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        response = manager.process(
            user_id,
            user_input
        )

        print(
            f"\nAI: {response}\n"
        )


if __name__ == "__main__":
    main()