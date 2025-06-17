import pytest
from typing import List

from log_parser.log import Log
from log_parser.event_detector import EventDetector
from log_parser.event_pattern import EventPattern
from tests.utils import make_log


@pytest.mark.parametrize(
    "logs, expected_event_count",
    [
        (  # valid single sequence
            [
                make_log("start", 0),
                make_log("continue", 2),
                make_log("finish", 4),
            ],
            1,
        ),
        (  # 2 separate sequences
            [
                make_log("start", 0),
                make_log("something else", 1),
                make_log("continue", 2),
                make_log("finish", 4),
                make_log("start", 5),
                make_log("something else", 6),
                make_log("continue", 7),
                make_log("finish", 9),
            ],
            2,
        ),
        (  # 2 separate sequences interleaved with noise
            [
                make_log("start", 0),
                make_log("something else", 1),
                make_log("start", 1),
                make_log("continue", 2),
                make_log("finish", 4),
                make_log("something else", 6),
                make_log("continue", 7),
                make_log("finish", 9),
            ],
            2,
        ),
        (  # one valid sequence, one partial sequence
            [
                make_log("start", 0),
                make_log("start", 1),
                make_log("continue", 2),
                make_log("finish", 4),
            ],
            1,
        ),
        (  # one valid sequence, one expired sequence
            [
                make_log("start", 0),
                make_log("start", 1),
                make_log("continue", 2),
                make_log("finish", 4),
                make_log("continue", 5),
                make_log("finish", 35),
            ],
            1,
        ),
        (  # 2 valid sequences, one expired sequence
            [
                make_log("start", 0),
                make_log("start", 1),
                make_log("continue", 2),
                make_log("start", 3),
                make_log("finish", 4),
                make_log("continue", 5),
                make_log("finish", 6),
                make_log("finish", 35),
            ],
            2,
        ),
    ],
)
def test_log_parser_single_event(
    sample_pattern: EventPattern, logs: List[Log], expected_event_count: int
):
    parser = EventDetector(event_patterns=[sample_pattern])
    detected_events = parser.detect_events(logs)
    assert len(detected_events) == expected_event_count

    for event in detected_events:
        assert event.name == sample_pattern.name
        assert event.duration <= sample_pattern.max_duration_seconds
