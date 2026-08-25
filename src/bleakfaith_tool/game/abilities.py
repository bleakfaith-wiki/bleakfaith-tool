from typing import Any

from bleakfaith_tool.game import Game
from bleakfaith_tool.unreal import paths


def make_map(value: dict[str, Any]) -> dict[str, str]:
    return {k.split("_")[0]: k for k in value}


class Ability:
    def __init__(self, key: str, value: dict[str, Any], game: Game) -> None:
        l10n = game.translations
        self.key: str = key
        keymap = make_map(value)
        self.object_path: str = paths.normalize(
            value[keymap["AbilityClass"]]["ObjectPath"]
        )
        self.is_passive: bool = value[keymap["IsPassive?"]]
        self.is_gear_passive: bool = value[keymap["IsGearPassive?"]]
        self.force_upgrade: bool = value[keymap["ForceUpgrade?"]]
        self.is_class_active: bool = value[keymap["IsClassActive?"]]
        self.unlocked_by: int | None = value[keymap["UnlockedBy_0"]]
        if self.unlocked_by and self.unlocked_by < 0:
            self.unlocked_by = None

        main_data = value[keymap["MainData"]]
        md_keymap = make_map(main_data)
        self.element: str = game.enum_display(main_data[md_keymap["Element"]])  # ty: ignore[invalid-assignment]
        self.type: str = game.enum_display(main_data[md_keymap["Type"]])  # ty: ignore[invalid-assignment]
        self.target: str = game.enum_display(main_data[md_keymap["Target"]])  # ty: ignore[invalid-assignment]

        inner_main = main_data[md_keymap["MainData"]]
        im_keymap = make_map(inner_main)
        self.is_weapon_based: bool = inner_main[im_keymap["IsWeaponBased?"]]

        names = inner_main[im_keymap["AbilityName"]]
        self.names: dict[str, str] = {}
        for entry in names:
            value = entry["Value"]
            if value and value != "" and value != "None":
                self.names[entry["Key"]] = l10n(value)

        descs = inner_main[im_keymap["AbilityDescription"]]
        self.descriptions: dict[str, str] = {}
        for entry in descs:
            value = entry["Value"]["SourceString"]
            if value and value != "" and value != "None":
                self.descriptions[entry["Key"]] = l10n(value)
        dmg_data = inner_main[im_keymap["DamageData"]]
        dmg_keymap = make_map(dmg_data)
        self.base_damage: float = dmg_data[dmg_keymap["BaseDamage"]]
        self.is_affected_bu_combos: bool = dmg_data[dmg_keymap["AffectedbyCombos"]]
