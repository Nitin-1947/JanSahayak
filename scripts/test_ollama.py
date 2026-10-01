from app.agent.brain import OllamaBrain


def main():

    brain = OllamaBrain()

    response = brain.generate(
        [
            {
                "role": "user",
                "content":
                    "नमस्ते, आप मेरी किस तरह सहायता कर सकते हैं?"
            }
        ]
    )

    print(response)


if __name__ == "__main__":
    main()