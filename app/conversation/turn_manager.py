class TurnManager:

    def __init__(self):

        self.current_speaker = None

    def start_user_turn(self):

        self.current_speaker = "user"

    def start_assistant_turn(self):

        self.current_speaker = "assistant"

    def end_turn(self):

        self.current_speaker = None