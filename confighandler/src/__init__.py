from datetime import datetime


def parse_date(date_str: str) -> datetime:
    """Parse a string to datetime using common formats."""
    date_formats = [
        "%d-%m-%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%d-%m-%Y",
    ]
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized for date: {date_str}")


EXPECTED_COLUMNS = {'id', 'name', 'description', 'type_id', 'value', 'debugmode'}
