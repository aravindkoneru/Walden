class WaldenException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class APIError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
