import pytest
from typing import List

from log_parser.log import Log
from log_parser.event_pattern import EventPattern
from log_parser.log_sequence_matcher import LogSequenceMatcher
from tests.utils import make_log


# Parametrize different full log sequences and expected result count
@pytest.mark.parametrize(
    "logs",
    [
        [  # valid full sequence
            make_log("start", 0),
            make_log("continue", 2),
            make_log("finish", 4),
        ],
        [  # noise in sequence
            make_log("start", 0),
            make_log("something else", 1),
            make_log("something else", 1),
            make_log("continue", 2),
            make_log("something else", 1),
            make_log("finish", 4),
        ],
    ],
)
def test_log_sequence_complete(basic_event_pattern: EventPattern, logs: List[Log]):
    sequence_handler = LogSequenceMatcher(basic_event_pattern, logs[0].timestamp)
    sequence_complete = False
    for log in logs:
        if sequence_handler.match_log(log) is not None:
            sequence_complete = True
            break
    assert sequence_complete


@pytest.mark.parametrize(
    "logs",
    [
        [  # missing step in sequence
            make_log("start", 0),
            make_log("finish", 4),
        ],
        [  # wrong order in sequence
            make_log("continue", 2),
            make_log("start", 0),
            make_log("finish", 4),
        ],
        [  # noise without matching sequence
            make_log("something else", 1),
            make_log("another irrelevant log", 3),
        ],
    ],
)
def test_log_sequence_incomplete(basic_event_pattern: EventPattern, logs: List[Log]):
    sequence_handler = LogSequenceMatcher(basic_event_pattern, logs[0].timestamp)
    for log in logs:
        assert sequence_handler.match_log(log) is None


def test_log_sequence_matcher_expiration(basic_event_pattern: EventPattern):
    start_log = make_log("start", 0)
    sequence_matcher = LogSequenceMatcher(basic_event_pattern, start_log.timestamp)
    sequence_matcher.match_log(start_log)

    # Log within the sequence duration
    current_log = make_log("continue", 10)
    assert sequence_matcher.match_log(current_log) is None

    # # Log that exceeds the max duration
    expired_log = make_log("finish", basic_event_pattern.max_duration_seconds + 1)
    with pytest.raises(TimeoutError):
        sequence_matcher.match_log(expired_log)
