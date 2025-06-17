from datetime import datetime

from log_parser.event_pattern import EventPattern
from log_parser.detected_event import DetectedEvent


class LogSequenceHandler:
    """
    LogSequenceHandler is responsible for managing a sequence of log entries
    that match a specific event pattern.
    """

    def __init__(self, event_pattern: EventPattern):
        self._event_pattern = event_pattern
        self._matched_logs = []
        self._start_time = None

    def handle(self, log: dict) -> bool:
        """
        Handles a log entry and checks if it matches the event pattern.
        Args:
            log (dict): A log entry

        Returns:
            bool: Whether the log entry was successfully handled.
        """
        if not self._event_pattern.matches_pattern_at_index(
            log["message"], len(self._matched_logs)
        ):
            return False

        self._matched_logs.append(log)
        if self._start_time is None:
            self._start_time = datetime.fromisoformat(log["timestamp"])
        return True

    def is_sequence_complete(self) -> bool:
        """
        Checks if the sequence of matched logs is complete
        Returns:
            bool: Whether the sequence of matched logs is complete.
        """
        return len(self._matched_logs) == len(self._event_pattern.sequence)

    def build_detected_event(self) -> DetectedEvent:
        """
        Builds a DetectedEvent object based on matched logs and event pattern
        Returns:
            DetectedEvent: An object representing the detected event
        """
        return DetectedEvent(
            name=self._event_pattern.name,
            matched_logs=self._matched_logs,
        )

    def has_expired(self, current_log_timestamp: str) -> bool:
        """
        Determines whether this handler is expired based on the current log
        timestamp

        Args:
            current_log_timestamp (datetime): The timestamp of the current log

        Returns:
            bool: Whether the handler has expired.
        """
        if self._start_time is None:
            return False
        time_since_start = (datetime.fromisoformat(current_log_timestamp) - self._start_time).total_seconds()
        return time_since_start > self._event_pattern.max_duration_seconds
