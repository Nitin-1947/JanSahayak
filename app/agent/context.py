class ConversationContext:

    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.messages = []

    def add_user(self, text: str):
        self.messages.append(
            {
                "role": "user",
                "content": text
            }
        )

        self._limit()

    def add_assistant(self, text: str):
        self.messages.append(
            {
                "role": "assistant",
                "content": text
            }
        )

        self._limit()

    def get_messages(self):
        return list(self.messages)

    def _limit(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[
                -self.max_messages:
            ]