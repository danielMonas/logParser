import pytest

from log_parser.log_sequence_handler import LogSequenceHandler
from tests.conftest import make_log


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
def test_log_sequence_handling_valid(sample_pattern, logs):
    sequence_handler = LogSequenceHandler(event_pattern=sample_pattern)
    for log in logs:
        sequence_handler.handle(log)
    assert sequence_handler.is_sequence_complete()


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
        [  # empty sequence
        ],
    ],
)
def test_log_sequence_handling_invalid(sample_pattern, logs):
    sequence_handler = LogSequenceHandler(event_pattern=sample_pattern)
    for log in logs:
        sequence_handler.handle(log)
    assert not sequence_handler.is_sequence_complete()


def test_log_sequence_handler_expiration(sample_pattern):
    sequence_handler = LogSequenceHandler(event_pattern=sample_pattern)
    start_log = make_log("start", 0)
    sequence_handler.handle(start_log)

    # Simulate a log that is within the max duration
    current_log = make_log("continue", 10)
    assert not sequence_handler.has_expired(current_log["timestamp"])

    # Simulate a log that exceeds the max duration
    expired_log = make_log("finish", sample_pattern.max_duration_seconds + 1)
    assert sequence_handler.has_expired(expired_log["timestamp"])
