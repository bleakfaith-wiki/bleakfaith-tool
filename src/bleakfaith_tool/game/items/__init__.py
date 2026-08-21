import json

from bleakfaith_tool.game import Game

from .item import Item


def load_from_guid_file(path: str, game: Game) -> dict[int, Item]:
    with open(path, "r") as f:
        guid_data = json.load(f)

    raw_data = guid_data["root"]["properties"]["InventoryData_0"]
    data = {i.key: i for i in (Item(d, game.translations) for d in raw_data)}

    return data
