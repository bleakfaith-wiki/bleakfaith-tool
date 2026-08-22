import json

from bleakfaith_tool.game import Game
from bleakfaith_tool.game.l10n import Translations

from .item import Item


def load_from_guid_file(path: str, game: Game) -> dict[int, Item]:
    with open(path, "r") as f:
        guid_data = json.load(f)

    raw_data = guid_data["root"]["properties"]["InventoryData_0"]
    data = {i.key: i for i in (Item(d, game.translations) for d in raw_data)}

    return data


class Items:
    def __init__(self, path: str, l10n: Translations) -> None:
        with open(path, "r") as f:
            guid_data = json.load(f)
        raw = guid_data["root"]["properties"]["InventoryData_0"]
        self.list = []
        self.by_guid: dict[int, Item] = {}
        self.by_id: dict[int, list[Item]] = {}
        self.by_id_base: dict[int, Item] = {}
        for raw_data in raw:
            item = Item(raw_data, l10n)
            self.list.append(item)
            self.by_guid[item.guid] = item
            if item.id not in self.by_id:
                self.by_id[item.id] = []
            self.by_id[item.id].append(item)
            if (
                item.id not in self.by_id_base
                or item.guid < self.by_id_base[item.id].guid
            ):
                self.by_id_base[item.id] = item

    def __iter__(self):
        yield from self.list

    def guid(self, guid: int) -> Item | None:
        return self.by_guid.get(guid)

    def id(self, id: int) -> list[Item] | None:
        return self.by_id.get(id)

    def id_first(self, id: int) -> Item | None:
        return self.by_id_base.get(id)

    def quest_id(self, quest_id: int) -> list[Item]:
        return [item for item in self.list if item.quest_id == quest_id]
