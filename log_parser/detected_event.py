from typing import List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DetectedEvent:
    """Class representing a detected event from log entries."""

    name: str
    matched_logs: List[dict]

    @property
    def duration(self) -> float:
        """Calculate the duration of the event in seconds."""
        return (self.end_time - self.start_time).total_seconds()

    @property
    def start_timestamp(self) -> datetime:
        """Get the start timestamp of the event."""
        return self.matched_logs[0]["timestamp"]

    @property
    def end_timestamp(self) -> datetime:
        """Get the end timestamp of the event."""
        return self.matched_logs[-1]["timestamp"]
