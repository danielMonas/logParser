from datetime import datetime


class Log:
    """
    Class representing a log entry with a message and a timestamp.
    """

    def __init__(self, message: str, timestamp: str):
        """
        Constructor

        Args:
            message (str): The log message.
            timestamp (str): The timestamp of the log entry in ISO format.
        """
        self.message = message
        self.timestamp = datetime.fromisoformat(timestamp)

    def __str__(self) -> str:
        return f"[{self.timestamp}]: {self.message}"
