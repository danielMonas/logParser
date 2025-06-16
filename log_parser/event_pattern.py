import re
from typing import List
from dataclasses import dataclass


@dataclass
class EventPattern:
    """
    Class representing a sequence of log patterns to detect an event.
    The sequence must be matched in order and within a specified duration.
    """

    name: str
    sequence: List[str]
    max_duration_seconds: int

    def __post_init__(self):
        self._compiled_patterns = [re.compile(p) for p in self.sequence]

    def matches_pattern_at_index(self, message: str, index: int = 0) -> bool:
        """
        Check if the message matches the pattern at the specified index
        Args:
            message (str): The log message to check.
            index (int, optional):  The index of the pattern to match against.
                                    Defaults to 0.
        Returns:
            bool: Whether the message matches the pattern at the specified index
        Raises:
            IndexError: If the index is out of range for the compiled pattern list
        """
        if not 0 <= index < len(self._compiled_patterns):
            raise IndexError("Index out of range for the compiled pattern list.")
        return bool(self._compiled_patterns[index].search(message))
