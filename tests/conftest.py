import pytest
from datetime import datetime
from log_parser.event_pattern import EventPattern

@pytest.fixture
def sample_pattern():
    return EventPattern(
        name="ExampleEvent",
        sequence=[r"start", r"continue", r"finish"],
        max_duration_seconds=30
    )

def make_log(message: str, offset_sec: int = 0) -> dict:
    current_time = datetime.now()
    log_time = datetime(year=current_time.year,
                        month=current_time.month,
                        day=current_time.day,
                        second=offset_sec)
    return {
        "timestamp": log_time.isoformat(),
        "message": message
    }
