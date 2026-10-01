def test_agent_import():

    from app.agent.brain import (
        OllamaBrain
    )

    assert OllamaBrain is not None