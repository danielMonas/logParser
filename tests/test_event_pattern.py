import pytest
from log_parser.event_pattern import EventPattern


@pytest.mark.parametrize("message", ["start", "user start session", ".start:"])
def test_matches_first_pattern(basic_event_pattern: EventPattern, message: str):
    assert basic_event_pattern.matches_pattern_at_index(message)


@pytest.mark.parametrize("message", ["noise", "", "ENd"])
def test_no_pattern_match(basic_event_pattern: EventPattern, message: str):
    assert not basic_event_pattern.matches_pattern_at_index(message, 2)


@pytest.mark.parametrize("message", ["start", "user start session", ".start:"])
def test_matches_pattern_incorrect_index(
    basic_event_pattern: EventPattern, message: str
):
    assert not basic_event_pattern.matches_pattern_at_index(message, 2)


def test_invalid_pattern_index(basic_event_pattern: EventPattern):
    with pytest.raises(IndexError):
        basic_event_pattern.matches_pattern_at_index("start", 993)
