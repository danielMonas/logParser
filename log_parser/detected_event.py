from typing import List
from datetime import datetime
from dataclasses import dataclass

from log_parser.log import Log


@dataclass
class DetectedEvent:
    """Class representing a detected event from log entries"""

    name: str
    matched_logs: List[Log]

    @property
    def duration(self) -> float:
        """
        Calculate the duration of the event in seconds

        Returns:
            float: Duration of the event in seconds
        """
        return (self.end_timestamp - self.start_timestamp).total_seconds()

    @property
    def start_timestamp(self) -> datetime:
        """
        Get the start timestamp of the event

        Returns:
            datetime: Start timestamp of the event
        """
        return self.matched_logs[0].timestamp

    @property
    def end_timestamp(self) -> datetime:
        """
        Get the end timestamp of the event

        Returns:
            datetime: End timestamp of the event
        """
        return self.matched_logs[-1].timestamp
