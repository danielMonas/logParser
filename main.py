import json
from typing import List
from typer import Typer

from log_parser.log import Log
from log_parser.event_pattern import EventPattern
from log_parser.event_detector import EventDetector
from log_parser.detected_event import DetectedEvent

app = Typer()

# NOTE: This is simply for demonstration purposes, and will not be used in production.


def load_logs(log_file_path: str) -> List[Log]:
    """
    Load logs from a JSON file

    Args:
        log_file_path (str): Path to the log file in JSON format.

    Returns:
        List[Log]: A list of Log objects parsed from the file.
    """
    with open(log_file_path, "r") as f:
        data = json.load(f)
    return [Log(item["message"], item["timestamp"]) for item in data]


def load_event_patterns(event_patterns_file_path: str) -> List[EventPattern]:
    """
    Load event patterns from a JSON file

    Args:
        event_patterns_file_path (str): Path to the event patterns file in JSON format

    Returns:
        List[EventPattern]: A list of EventPattern objects parsed from the file
    """
    with open(event_patterns_file_path, "r") as f:
        data = json.load(f)
    return [
        EventPattern(item["name"], item["sequence"], item["max_duration"])
        for item in data
    ]


@app.command()
def parse_logs(log_file_path: str, patterns_file_path: str) -> None:
    """
    Parse logs from a file using specified event patterns and print detected events

    Args:
        log_file_path (str): Path to the log file in JSON format
        patterns_file_path (str): Path to the event patterns file in JSON format
    """
    # Load logs and patterns
    logs = load_logs(log_file_path)
    patterns = load_event_patterns(patterns_file_path)

    # Detect events
    detector = EventDetector(event_patterns=patterns)
    detected_events: List[DetectedEvent] = detector.detect_events(logs)

    print(f"Detected {len(detected_events)} events:")
    for event in detected_events:
        print(
            f"Event: {event.name}, Duration: {event.duration} seconds, Start: {event.start_timestamp}, End: {event.end_timestamp}"
        )


def main():
    app()


if __name__ == "__main__":
    main()
