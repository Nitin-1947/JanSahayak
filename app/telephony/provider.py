class TelephonyProvider:

    def answer_call(
        self,
        call_id: str
    ):
        raise NotImplementedError

    def hangup_call(
        self,
        call_id: str
    ):
        raise NotImplementedError

    def play_audio(
        self,
        call_id: str,
        audio_url: str
    ):
        raise NotImplementedError