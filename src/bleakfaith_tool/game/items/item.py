from bleakfaith_tool.game.l10n import Translations
from bleakfaith_tool.game.parsing import non_neg


def none_str(s: str | None) -> str | None:
    return None if s in ("None", "null", "") else s


def extract_string(data: dict[str, dict[str, dict[str, str]]]) -> str:
    var = data["variant"]

    if "None" in var:
        return var["None"]["culture_invariant"]

    if "Base" in var:
        return var["Base"]["source_string"]

    raise ValueError("string object not 'None' or 'Base'")


class Item:
    def __init__(self, data: dict, l10n: Translations) -> None:
        self.key: int = data["key"]
        value = data["value"]
        self.id: int = value["ItemId_0"]
        self.guid: int = value["ItemGUID_0"]
        self.max_stack: int = value["MaxStack_0"]
        self.is_unique: bool = value["Unique_0"]
        self.name: str = l10n(extract_string(value["Name_0"]))
        self.description: str = l10n(extract_string(value["Description_0"]))
        self.types: list[str] = value["ItemType_0"]
        self.required_other_slots: list[str] = value["DoesRequireAnotherSlot_0"]
        self.quest_id: int | None = non_neg(value["QuestID_0"])
        self.sprite: str | None = none_str(value["Sprite_0"])
        self.is_fragmented: bool = value["Fragmented_0"]
        self.weight: float = value["ItemWeight_0"]
        self.tier: int = value["Tier_0"]
        self.armor_data = ArmorData(value["ArmorData_0"])
        self.weapon_data = WeaponData(value["WeaponData_0"])
        self.consumable_data = ConsumableData(value["ConsumableData_0"])
        self.fragment_data = FragmentData(value["FragmentData_0"], l10n)

    def __str__(self) -> str:
        return f'InventoryItem(guid={self.guid}, name="{self.name}")'

    def __repr__(self) -> str:
        return f'InventoryItem(guid={self.guid}, name="{self.name}")'


class ArmorData:
    def __init__(self, data: dict) -> None:
        self.mesh: str | None = none_str(data.get("ArmorMesh_0"))
        self.sharp: float = data["SharpWeaponRessistance_0"]
        self.blunt: float = data["BluntWeaponRessistance_0"]
        self.techno: float = data["TechnoWeaponRessistance_0"]
        self.sharp_multiplier: float = data["SharpWeaponRessistanceMultiplier_0"]
        self.blunt_multiplier: float = data["BluntWeaponRessistanceMultiplier_0"]
        self.techno_multiplier: float = data["TechnoWeaponRessistanceMultiplier_0"]
        self.tier: int = data["Tier_0"]
        self.slot: str = data["Slot_0"]
        self.weight: str = data["ArmorWeight_0"]
        self.fragment_slot_data: FragmentSlotData = FragmentSlotData(
            data["FragmentSlotData_0"]
        )
        self.should_auto_hide_mask: bool = data["ShouldAutoHideMask_0"]
        self.helmet_compactability: str = data["HelmetCompactability_0"]
        self.armor_mask: str = data["ArmorMask_0"]


class WeaponData:
    def __init__(self, data: dict) -> None:
        self.damage_min: float = data["MinDamage_0"]
        self.damage_max: float = data["MaxDamage_0"]
        self.speed: str = data["WeaponSpeed_0"]
        self.type: str = data["WeaponType_0"]
        self.sharpness: str = data["Sharpness_0"]
        self.can_generate_hit: bool = data["CanGenerateHit_0"]
        self.fragment_slot_data = FragmentSlotData(data["FragmentSlotData_0"])
        self.holster_locations: list[str] = data["HolsterLocations_0"]
        self.primary_class_reference: str | None = none_str(
            data["PrimaryClassRefference_0"]
        )
        self.secondary_class_reference: str | None = none_str(
            data["SecondaryClassRefference_0"]
        )
        # TODO: SpecialData_0
        self.primary_custom_slot: str = data["PrimaryCustomSlot_0"]
        self.secondary_custom_slot: str = data["SecondaryCustomSlot_0"]
        self.holster_slots: list[str] = data["HolsterSlots_0"]


class ConsumableData:
    def __init__(self, data: dict) -> None:
        self.type: str = data["ConsumableType_0"]


class FragmentData:
    def __init__(self, data: dict, l10n: Translations) -> None:
        self.name: str = l10n(extract_string(data["Name_0"]))
        self.description: str = l10n(extract_string(data["Description_0"]))
        self.type: str = data["Type_0"]
        self.tier: int = data["Tier_0"]
        self.stat_data = FragmentStatData(data["StatData_0"])
        self.ability_data = FragmentAbilityData(data["AbilityData_0"])
        self.class_data = FragmentClassData(data["ClassData_0"])
        self.quest_id: int = data["QuestID_0"]
        self.icon: str | None = none_str(data["Icon_0"])


class FragmentStatData:
    def __init__(self, data: dict) -> None:
        self.armor: dict[str, int] = {}
        for idx, attr in enumerate(data["StatArmorIncrease_0"]):
            self.armor[attr] = data["StatArmorIncreaseAmount_0"][idx]
        self.weapon: dict[str, int] = {}
        for idx, attr in enumerate(data["StatWeaponIncrease_0"]):
            self.weapon[attr] = data["StatWeaponIncreaseAmount_0"][idx]


class FragmentAbilityData:
    def __init__(self, data: dict) -> None:
        # TODO: Figure out what this contains
        self.ability = {
            "old": {
                "asset_path_name": none_str(
                    data["Ability_0"]["Old"]["asset_path_name"]
                ),
                "sub_path_string": none_str(
                    data["Ability_0"]["Old"]["sub_path_string"]
                ),
            }
        }
        # TODO: Figure out what it contains
        self.acceptable_weapons: list = data["AcceptableWeapons_0"]


class FragmentClassData:
    def __init__(self, data: dict) -> None:
        self.is_passive: bool = data["isPassive_0"]
        # TODO: Figure out what it contains
        self.abilities: list = data["Abilities_0"]


class FragmentSlotData:
    def __init__(self, data: dict) -> None:
        self.can_be_edited: bool = data["CanBeEdited_0"]
        self.number_of_available_stat_slots: int = data["NumberOfAvaliableStatSlots_0"]
        self.stat_fragment_ids: list[int] = data["StatFragmentID_0"]
        self.number_of_available_ability_slots: int = data[
            "NumberOfAvaliableAbilitySlots_0"
        ]
        self.ability_fragment_ids: list[int] = data["AbilityFragmentID_0"]
