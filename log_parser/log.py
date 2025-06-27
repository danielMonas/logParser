from datetime import datetime


class Log:
    """
    Class representing a log entry
    """

    def __init__(self, message: str, timestamp_iso: str):
        """
        Constructor

        Args:
            message (str): The log message.
            timestamp_iso (str): The timestamp of the log entry in ISO format.
        """
        self.message = message
        self.timestamp = datetime.fromisoformat(timestamp_iso)

    def __str__(self) -> str:
        return f"[{self.timestamp}]: {self.message}"
