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
                make_log("continue", 3),
                # Note: Since this log completes a sequences, it will be processed
                # exactly once, which means that the second ongoing sequence
                # will not be counted as a complete sequence.
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
def test_event_detector_single_event(
    basic_event_pattern: EventPattern, logs: List[Log], expected_event_count: int
):
    detector = EventDetector(event_patterns=[basic_event_pattern])
    detected_events = detector.detect_events(logs)

    assert len(detected_events) == expected_event_count
    for event in detected_events:
        assert event.name == basic_event_pattern.name
        assert event.duration <= basic_event_pattern.max_duration_seconds


@pytest.mark.parametrize(
    "logs, expected_event_count",
    [
        (  # Exactly one valid sequence
            [
                make_log("start", 0),
                make_log("b", 2),
                make_log("end", 3),
                make_log("other end", 4),
            ],
            1,
        ),
        (  # Two sequences from the same starting log
            [
                make_log("start", 0),
                make_log("b", 2),
                make_log("something else", 2),
                make_log("Second pattern", 3),
                make_log("other end", 4),
            ],
            2,
        ),
    ],
)
def test_event_detector_multiple_patterns_same_start(
    logs: List[Log], expected_event_count: int
):
    patterns = [
        EventPattern(
            name="Pattern2",
            sequence=["start", ".*something.*", "Second pattern"],
            max_duration_seconds=15,
        ),
        EventPattern(
            name="Pattern1", sequence=["start", "b", ".*end"], max_duration_seconds=10
        ),
    ]

    detector = EventDetector(event_patterns=patterns)
    detected_events = detector.detect_events(logs)

    assert len(detected_events) == expected_event_count
