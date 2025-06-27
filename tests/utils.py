from datetime import datetime

from log_parser.log import Log


def make_log(message: str, offset_seconds: int = 0) -> Log:
    """
    Create a log entry with a specific message and an optional offset in seconds
    from the current day, to simulate log timestamps.

    Args:
        message (str): The log message.
        offset_seconds (int, optional): The number of seconds to offset the log
        time. Defaults to 0.

    Returns:
        Log: A Log object with the specified message and timestamp
    """
    current_time = datetime.now()
    log_time = datetime(
        year=current_time.year,
        month=current_time.month,
        day=current_time.day,
        second=offset_seconds,
    )
    return Log(message, log_time.isoformat())
