class SilenceDetector:

    def __init__(
        self,
        threshold_seconds: float = 1.5
    ):

        self.threshold_seconds = (
            threshold_seconds
        )

    def is_silent(
        self,
        duration: float
    ):

        return (
            duration
            >= self.threshold_seconds
        )