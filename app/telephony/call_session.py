class CallSession:
    def __init__(self, call_id: str, user_id: str):
        self.call_id = call_id
        self.user_id = user_id
        self.active = True

    def end(self):
        self.active = False
