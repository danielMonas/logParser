import pytest

from log_parser.event_pattern import EventPattern


@pytest.fixture
def basic_event_pattern():
    return EventPattern(
        name="ExampleEvent",
        sequence=[r".*start.*", r"continue", r"finish"],
        max_duration_seconds=30,
    )
