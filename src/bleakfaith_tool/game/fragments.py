from dataclasses import dataclass
from enum import Enum
from typing import Any

from bleakfaith_tool.game import Game


def make_map(value: dict[str, Any]) -> dict[str, str]:
    return {k.split("_")[0]: k for k in value}


class FragmentType(Enum):
    ABILITY = "Ability"
    STAT = "Stat"

    @staticmethod
    def parse(s: str) -> FragmentType:
        match s:
            case "EFragmentType::VE_Ability":
                return FragmentType.ABILITY
            case "EFragmentType::VE_Stat":
                return FragmentType.STAT
            case _:
                raise ValueError(f"Unknown fragment type: {s}")


class Fragment:
    def __init__(self, key: str, value: dict[str, Any], game: Game) -> None:
        l10n = game.translations
        self.id = int(key)
        keymap = make_map(value)
        self.is_debug: bool = value.get(keymap["IsDebug"], False)
        data = value[keymap["Data"]]
        self.name: str = l10n(data["Name"]["SourceString"])
        self.description: str = l10n(data["Description"]["SourceString"])
        self.type: FragmentType = FragmentType.parse(data["FragmentType"])
        self.tier: int = data["Tier"]
        self.ability_data: FragmentAbilityData | None = None
        self.stat_data: FragmentStatData | None = None
        if self.type == FragmentType.ABILITY:
            self.ability_data = FragmentAbilityData(data["AbilityData"])
        elif self.type == FragmentType.STAT:
            self.stat_data = FragmentStatData(data["StatData"])


class FragmentAbilityData:
    def __init__(self, data: dict[str, Any]) -> None:
        self.is_passive: bool = data["ClassData"]["isPassive"]
        self.quest_id: int = data["QuestID"]
        self.acceptable_weapons: list[str] = data["AcceptableWeapons"]


class FragmentStatData:
    def __init__(self, data: dict[str, Any]) -> None:
        assert len(data["StatArmorIncrease"]) == 1
        assert len(data["StatArmorIncreaseAmount"]) == 1
        assert len(data["StatWeaponIncrease"]) == 1
        assert len(data["StatWeaponIncreaseAmount"]) == 1
        self.armor: FragmentStatAttributeData = FragmentStatAttributeData(
            data["StatArmorIncrease"][0], data["StatArmorIncreaseAmount"][0]
        )
        self.weapon: FragmentStatAttributeData = FragmentStatAttributeData(
            data["StatWeaponIncrease"][0], data["StatWeaponIncreaseAmount"][0]
        )


@dataclass
class FragmentStatAttributeData:
    attribute: str
    amount: float
