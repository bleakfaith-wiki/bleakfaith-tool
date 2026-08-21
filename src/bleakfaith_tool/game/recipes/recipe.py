from bleakfaith_tool.game import Game
from bleakfaith_tool.game.parsing import non_neg


def compact(list: list[str | None]) -> list[str]:
    return [s for s in list if s is not None and s != "None" and s != "null"]


class Recipe:
    def __init__(self, key: str, data: dict, game: Game) -> None:
        self.key = key
        data = {k.split("_")[0]: v for k, v in data.items()}
        self.type: str = game.enum_display(data["Type"]) or data["Type"]
        self.craft: list[str] = compact(
            [game.enum_display(n) or n for n in data["Craft"]]
        )
        self.unlock: list[str] = compact(
            [game.enum_display(n) or n for n in data["Unlock"]]
        )
        self.needed_item: int | None = non_neg(data["NeededItem"])
        self.name: str = game.translate(data["Name"])
        self.item_id: int = data["ItemID"]
        self.per_craft: int = data["PerCraft"]
        self.materials = {
            e["MaterialID"]: e["MaterialAmount"]
            for e in [
                {k.split("_")[0]: v for k, v in m.items()} for m in data["Materials"]
            ]
        }
