import re
from typing import List


class EventPattern:
    """
    Class representing a sequence of log patterns to detect an event.
    The sequence must be matched in order and within a specified duration.
    """

    def __init__(self, name: str, sequence: List[str], max_duration_seconds: int):
        """
        Initialize the EventPattern with a name, sequence of patterns, and maximum duration.

        Args:
            name (str): The name of the event pattern.
            sequence (List[str]): A list of regex patterns that define the sequence.
            max_duration_seconds (int): The maximum duration in seconds for the sequence to be matched.
        """
        self.name = name
        self.sequence = [re.compile(p) for p in sequence]
        self.max_duration_seconds = max_duration_seconds

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
        if 0 <= index < len(self.sequence):
            return self.sequence[index].match(message) is not None
        raise IndexError(f"Index ({index}) out of range for the compiled pattern list.")
