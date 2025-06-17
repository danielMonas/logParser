from datetime import datetime

from log_parser.event_pattern import EventPattern
from log_parser.detected_event import DetectedEvent
from log_parser.log import Log


class LogSequenceMatcher:
    """
    OngoingLogSequence is responsible for managing the state of a sequence of
    log entries that match a specific event pattern over time.
    The sequence is considered expired if the time since its creation exceeds
    the maximum duration defined in the event pattern.
    """

    def __init__(self, event_pattern: EventPattern, start_time: datetime):
        self._event_pattern = event_pattern
        self._start_time = start_time
        self._matched_logs = []

    def process_log(self, log: Log) -> bool:
        """
        Handles a log entry and checks if it matches the event pattern.
        Args:
            log (Log): A log entry

        Returns:
            bool: Whether the sequence is complete after handling this log.
        """
        # Check if the log matches the pattern at the current index. If it does not,
        if self._event_pattern.matches_pattern_at_index(
            log.message, len(self._matched_logs)
        ):
            self._matched_logs.append(log)

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

    def has_expired(self, current_log_timestamp: datetime) -> bool:
        """
        Determines whether this sequence is expired based on the current log
        timestamp

        Args:
            current_log_timestamp (datetime): The timestamp of the current log

        Returns:
            bool: Whether the sequence has expired.
        """
        time_since_start = (current_log_timestamp - self._start_time).total_seconds()
        return time_since_start > self._event_pattern.max_duration_seconds
