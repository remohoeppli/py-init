class SetupException(Exception):
    """Custom setup exception"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.message:
            return f"SetupException, {self.message} "
        else:
            return "SetupException has been raised"
