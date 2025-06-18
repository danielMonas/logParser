from typing import List

from log_parser.log import Log
from log_parser.event_pattern import EventPattern
from log_parser.detected_event import DetectedEvent
from log_parser.log_sequence_matcher import LogSequenceMatcher


class EventDetector:
    """
    The purpose of this class is to parse log entries and detect events based
    on defined patterns.
    """

    def __init__(self, event_patterns: List[EventPattern]):
        """Initialize the LogParser with a list of event patterns."""
        self._event_patterns = event_patterns
        self._matchers = []

    def detect_events(self, logs: List[Log]) -> List[DetectedEvent]:
        """
        Detect events in the provided logs based on the defined event patterns.

        Args:
            logs (List[Log]): A list of log entries
        """
        detected_events = []
        for log in logs:
            # Check if the log message matches the start of any event pattern
            # If it does, create a new sequence matcher for that pattern to
            # try and continue matching subsequent logs in the sequence.
            for pattern in self._event_patterns:
                if pattern.matches_pattern_at_index(log.message):
                    self._matchers.append(LogSequenceMatcher(pattern, log.timestamp))
            # Process the current log entry against all active handlers
            detected_events += self._try_match_log(log)
        return detected_events

    def _try_match_log(self, log: Log) -> List[DetectedEvent]:
        """
        Try to match the current log entry against all active sequence matchers.
        If a matcher completes a sequence or expires, it is removed from the list of matchers.

        Args:
            log (Log): The current log entry to process.

        Returns:
            List[DetectedEvent]: A list of detected events from the processed matchers.
        """
        matchers_to_remove = []
        detected_events = []

        for matcher in self._matchers:
            try:
                detected_event = matcher.match_log(log)
                if detected_event:
                    detected_events.append(detected_event)
                    matchers_to_remove.append(matcher)
                    break
            except TimeoutError:
                matchers_to_remove.append(matcher)

        self._matchers = [m for m in self._matchers if m not in matchers_to_remove]
        return detected_events
