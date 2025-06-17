from typing import List

from log_parser.log import Log
from log_parser.event_pattern import EventPattern
from log_parser.detected_event import DetectedEvent
from log_parser.log_sequence_matcher import LogSequenceMatcher


class EventDetector:
    """
    LogParser class to parse log entries and detect events based on defined patterns.
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
            # If it does, create a new LogSequenceHandler for that pattern
            for pattern in self._event_patterns:
                if pattern.matches_pattern_at_index(log.message):
                    self._matchers.append(LogSequenceMatcher(pattern, log.timestamp))
            # Process the current log entry against all active handlers
            detected_events += self._process_handlers(log)
        return detected_events

    def _process_handlers(self, log: Log) -> List[DetectedEvent]:
        """
        Process the current log entry against all active handlers.
        If a handler completes a sequence or expires, it is removed from the list of handlers.

        Args:
            log (Log): The current log entry to process.

        Returns:
            List[DetectedEvent]: A list of detected events from the processed handlers.
        """
        matchers_to_remove = []
        detected_events = []
        for matcher in self._matchers:
            if matcher.has_expired(log.timestamp):
                matchers_to_remove.append(matcher)
            elif matcher.process_log(log):
                detected_events.append(matcher.build_detected_event())
                matchers_to_remove.append(matcher)
                # If the current log completes a sequence, we stop processing
                # other handles for this log entry.
                # This means that the same log cannot be part of multiple sequences.
                # This is a design choice to avoid ambiguity in event detection.
                break
        self._matchers = [m for m in self._matchers if m not in matchers_to_remove]
        return detected_events
