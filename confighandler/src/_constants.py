from typing import Any, Callable
import locale
from datetime import datetime
from . import parse_date

# Type mapping functions
TYPE_MAPPERS: dict[int, Callable[[str], Any]] = {
    1: str,  # String
    2: int,  # Integer
    3: locale.atof,  # Float
    4: lambda x: x.lower() in ("y", "yes", "t", "true", "on", "1", "ja"),  # Boolean
    5: lambda x: x.split(","),  # String list
    6: lambda x: [int(val) for val in x.split(",")],  # Integer list
    7: lambda x: [locale.atof(val) for val in x.split(",")],  # Float list
    8: parse_date,  # Date
}


# Add this type mapping dictionary near your other type mappings
TYPE_DEFINITIONS: dict[int, type] = {
    1: str,  # String
    2: int,  # Integer
    3: float,  # Float
    4: bool,  # Boolean
    5: list[str],  # String list
    6: list[int],  # Integer list
    7: list[float],  # Float list
    8: datetime,  # Date
}
