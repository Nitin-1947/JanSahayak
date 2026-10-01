class InterruptionManager:

    def __init__(self):

        self.interrupted = False

    def interrupt(self):

        self.interrupted = True

    def reset(self):

        self.interrupted = False

    def is_interrupted(self):

        return self.interrupted