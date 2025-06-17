from typing import List, Dict

from log_parser.event_pattern import EventPattern
from log_parser.detected_event import DetectedEvent
from log_parser.log_sequence_handler import LogSequenceHandler


class LogParser:
    """
    LogParser class to parse log entries and detect events based on defined patterns.
    """

    def __init__(self, event_patterns: List[EventPattern]):
        """Initialize the LogParser with a list of event patterns."""
        self._event_patterns = event_patterns
        self._detected_events = []
        self._handlers = []

    def parse(self, logs: List[Dict[str, str]]) -> None:
        """Parse a list of log entries and detect events based on the defined patterns.

        Args:
            logs (List[Dict[str, str]]): A list of log entries, each represented as a dictionary with 'timestamp' and 'message'.
        """
        for log in logs:
            for pattern in self._event_patterns:
                if pattern.matches_pattern_at_index(log["message"]):
                    self._handlers.append(LogSequenceHandler(pattern))
            self._process_handlers(log)

    def get_detected_events(self) -> List[DetectedEvent]:
        """Get the list of detected events.

        Returns:
            List[DetectedEvent]: A list of DetectedEvent objects representing the detected events.
        """
        return self._detected_events

    def _process_handlers(self, log: Dict[str, str]) -> None:
        """
        Process the current log entry against all active handlers.
        If a handler completes a sequence or expires, it is removed from the list of handlers.

        Args:
            log (Dict[str, str]): The current log entry to process.
        """
        handlers_to_remove = []
        for handler in self._handlers:
            if handler.has_expired(log["timestamp"]):
                handlers_to_remove.append(handler)
            elif handler.handle(log):
                if handler.is_sequence_complete():
                    self._detected_events.append(handler.build_detected_event())
                    handlers_to_remove.append(handler)
                    break

        for handler in handlers_to_remove:
            self._handlers.remove(handler)
