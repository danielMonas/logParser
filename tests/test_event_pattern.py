import pytest
from log_parser.event_pattern import EventPattern


@pytest.mark.parametrize("message", ["start", "user start session", ".start:"])
def test_matches_first_step(sample_pattern: EventPattern, message: str):
    assert sample_pattern.matches_pattern_at_index(message)


@pytest.mark.parametrize("message", ["noise", "", "ENd"])
def test_matches_wrong_step(sample_pattern: EventPattern, message: str):
    assert not sample_pattern.matches_pattern_at_index(message, 2)
