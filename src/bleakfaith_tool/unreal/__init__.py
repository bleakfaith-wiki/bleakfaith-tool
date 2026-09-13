from dataclasses import dataclass
from typing import Any

from .data_table import DataTable as DataTable
from .enum import EnumEntry as EnumEntry
from .enum import UserDefinedEnum as UserDefinedEnum

# type BlueprintGeneratedClass = list[dict]


@dataclass
class BlueprintGeneratedClass:
    name: str
    path: str
    data: list[dict[str, Any]]
