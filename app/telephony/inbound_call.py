class InboundCallHandler:

    def handle(
        self,
        call_data: dict
    ):

        return {
            "status": "received",
            "call_data": call_data
        }