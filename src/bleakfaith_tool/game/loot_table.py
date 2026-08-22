from dataclasses import dataclass
from typing import Any

from bleakfaith_tool.unreal import DataTable


def transform_keys(dict: dict) -> dict[str, str]:
    return {k.split("_")[0]: k for k in dict}


def loot_tables_from_data_table(data_table: DataTable) -> dict[int, LootTable]:
    return {int(k.split("_")[1]): LootTable(k, v) for k, v in data_table.rows.items()}


class LootTable:
    def __init__(self, key: str, data: dict[str, Any]) -> None:
        self.id: int = int(key.split("_")[1])
        dkmap = transform_keys(data)
        self.note: str = data[dkmap["DeveloperNote"]]
        content = data[dkmap["Data"]]
        ckmap = transform_keys(content)
        items = content[ckmap["ItemsInSet"]]
        pcts = content[ckmap["PercentagePerSet"]]
        mins = content[ckmap["MinAmount"]]
        maxs = content[ckmap["MaxAmount"]]
        self.entries: list[LootTableEntry] = []
        for idx, item in enumerate(items):
            if item == -1:
                break
            rate = pcts[idx] / 100.0
            self.entries.append(LootTableEntry(item, rate, mins[idx], maxs[idx]))


@dataclass
class LootTableEntry:
    item_id: int
    rate: float
    min: int
    max: int
