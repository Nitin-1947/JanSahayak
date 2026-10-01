class Authentication:

    def verify(
        self,
        token: str
    ):

        return bool(token)