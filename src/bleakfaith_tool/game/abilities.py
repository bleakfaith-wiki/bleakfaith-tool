from typing import Any

import structlog

from bleakfaith_tool.game import Game
from bleakfaith_tool.game.fragments import Fragment
from bleakfaith_tool.unreal import DataTable, paths

LOG = structlog.get_logger()


def make_map(value: dict[str, Any]) -> dict[str, str]:
    return {k.split("_")[0]: k for k in value}


def abilities_from_data_table(
    data_table: DataTable, game: Game, fragments: dict[str, Fragment]
) -> dict[str, Ability]:
    return {k: Ability(k, v, game, fragments) for k, v in data_table.rows.items()}


class Ability:
    def __init__(
        self,
        key: str,
        value: dict[str, Any],
        game: Game,
        fragments: dict[str, Fragment],
    ) -> None:
        l10n = game.translations
        keymap = make_map(value)
        self.object_path: str = paths.normalize(
            value[keymap["AbilityClass"]]["ObjectPath"]
        )
        search_path = f"/{self.object_path}"
        search_path = search_path[: search_path.rfind(".")]
        fragment = fragments.get(search_path)
        # TODO: Theory: Only abilities that appear on weapons have a corresponding fragment?
        self.fragment_id: int | None = fragment.id if fragment else None
        self.key: str = key
        self.is_passive: bool = value[keymap["IsPassive?"]]
        self.is_gear_passive: bool = value[keymap["IsGearPassive?"]]
        self.force_upgrade: bool = value[keymap["ForceUpgrade?"]]
        self.is_class_active: bool = value[keymap["IsClassActive?"]]
        self.unlocked_by: int | None = value.get(keymap.get("UnlockedBy_0"))
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
        self.is_affected_by_combos: bool = dmg_data[dmg_keymap["AffectedbyCombos"]]
