from bleakfaith_tool.game.items.types import (
    ArmorWeight,
    DamageType,
    ItemType,
    Sharpness,
    WeaponSpeed,
    WeaponType,
)
from bleakfaith_tool.game.l10n import Translations
from bleakfaith_tool.game.parsing import non_neg

TYPE_MAP = {
    "EItemType::VE_Blueprint": ItemType.BLUEPRINT,
    "EItemType::VE_Consumable": ItemType.CONSUMABLE,
    "EItemType::VE_EquipAmulet": ItemType.AMULET,
    "EItemType::VE_EquipCape": ItemType.CAPE,
    "EItemType::VE_EquipChest": ItemType.CHEST,
    "EItemType::VE_EquipGloves": ItemType.GLOVES,
    "EItemType::VE_EquipHelm": ItemType.HELMET,
    "EItemType::VE_EquipLegs": ItemType.LEGS,
    "EItemType::VE_EquipRing1": ItemType.RING,
    "EItemType::VE_EquipRing2": ItemType.RING,
    "EItemType::VE_EquipShoulder": ItemType.SHOULDER,
    "EItemType::VE_EquipWeaponLeft": ItemType.WEAPON,
    "EItemType::VE_EquipWeaponLeftSecondary": ItemType.WEAPON,
    "EItemType::VE_EquipWeaponRight": ItemType.WEAPON,
    "EItemType::VE_EquipWeaponRightSecondary": ItemType.WEAPON,
    "EItemType::VE_Fragment": ItemType.FRAGMENT,
    "EItemType::VE_Material": ItemType.MATERIAL,
    "EItemType::VE_QuestItem": ItemType.QUEST_ITEM,
    "EItemType::VE_Resource": ItemType.RESOURCE,
    "EItemType::VE_Usable": ItemType.USABLE,
}

SPEED_MAP = {
    "EWeaponSpeed::VE_Fast": WeaponSpeed.FAST,
    "EWeaponSpeed::VE_Slow": WeaponSpeed.SLOW,
    "EWeaponSpeed::VE_Sluggish": WeaponSpeed.SLUGGISH,
    "EWeaponSpeed::VE_Swift": WeaponSpeed.SWIFT,
}

WEAPON_TYPE_MAP = {
    "EWeaponType::VE_Claw": WeaponType.CLAW,
    "EWeaponType::VE_Crossbow": WeaponType.CROSSBOW,
    "EWeaponType::VE_DualBlades": WeaponType.DUAL_BLADES,
    "EWeaponType::VE_DualDaggers": WeaponType.DUAL_DAGGERS,
    "EWeaponType::VE_DualSickles": WeaponType.DUAL_SICKLES,
    "EWeaponType::VE_Fang": WeaponType.FANG,
    "EWeaponType::VE_Gauntlent": WeaponType.GAUNTLET,
    "EWeaponType::VE_GreatAxe": WeaponType.GREAT_AXE,
    "EWeaponType::VE_GreatMace": WeaponType.GREAT_MACE,
    "EWeaponType::VE_GreatSword": WeaponType.GREAT_SWORD,
    "EWeaponType::VE_Halberd": WeaponType.HALBERD,
    "EWeaponType::VE_Longbow": WeaponType.LONGBOW,
    "EWeaponType::VE_OneHandedAxe": WeaponType.ONE_HANDED_AXE,
    "EWeaponType::VE_OneHandedLance": WeaponType.ONE_HANDED_LANCE,
    "EWeaponType::VE_OneHandedMace": WeaponType.ONE_HANDED_MACE,
    "EWeaponType::VE_OneHandedPick": WeaponType.ONE_HANDED_PICK,
    "EWeaponType::VE_OneHandedStaff": WeaponType.ONE_HANDED_STAFF,
    "EWeaponType::VE_OneHandedSword": WeaponType.ONE_HANDED_SWORD,
    "EWeaponType::VE_Shield": WeaponType.SHIELD,
    "EWeaponType::VE_Spear": WeaponType.SPEAR,
    "EWeaponType::VE_Staff": WeaponType.STAFF,
    "EWeaponType::VE_Tail": WeaponType.TAIL,
    "EWeaponType::VE_Torch": WeaponType.TORCH,
    "EWeaponType::VE_Twinblade": WeaponType.TWINBLADE,
    "EWeaponType::VE_TwoHandedAxe": WeaponType.TWO_HANDED_AXE,
    "EWeaponType::VE_TwoHandedMace": WeaponType.TWO_HANDED_MACE,
    "EWeaponType::VE_TwoHandedScythe": WeaponType.TWO_HANDED_SCYTHE,
    "EWeaponType::VE_TwoHandedSword": WeaponType.TWO_HANDED_SWORD,
}

SHARPNESS_MAP = {
    "EWeaponSharpness::VE_Blunt": Sharpness.BLUNT,
    "EWeaponSharpness::VE_Sharp": Sharpness.SHARP,
}

ARMOR_WEIGHT_MAP = {
    "EArmorWeight::VE_Light": ArmorWeight.LIGHT,
    "EArmorWeight::VE_Medium": ArmorWeight.MEDIUM,
    "EArmorWeight::VE_Heavy": ArmorWeight.HEAVY,
    "EArmorWeight::VE_Cloth": ArmorWeight.CLOTH,
}


def clean_name(name: str) -> str:
    return name.replace("’", "'")


def none_str(s: str | None) -> str | None:
    return None if s in ("None", "null", "") else s


def extract_string(data: dict[str, dict[str, dict[str, str]]]) -> str:
    var = data["variant"]

    if "None" in var:
        return var["None"]["culture_invariant"]

    if "Base" in var:
        return var["Base"]["source_string"]

    raise ValueError("string object not 'None' or 'Base'")


def parse_types(types: list[str]) -> set[ItemType]:
    return {TYPE_MAP[t] for t in types if t in TYPE_MAP}


class Item:
    def __init__(self, data: dict, l10n: Translations) -> None:
        self.key: int = data["key"]
        value = data["value"]
        self.id: int = value["ItemId_0"]
        self.guid: int = value["ItemGUID_0"]
        self.max_stack: int = value["MaxStack_0"]
        self.is_unique: bool = value["Unique_0"]
        self.name: str = clean_name(l10n(extract_string(value["Name_0"]))).strip()
        self.description: str | None = l10n(extract_string(value["Description_0"]))
        if self.description is not None:
            self.description = self.description.strip()
        self.types: list[ItemType] = list(parse_types(value["ItemType_0"]))
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

    @property
    def is_weapon(self) -> bool:
        if ItemType.WEAPON not in self.types:
            return False

        return self.weapon_data.type not in (None, WeaponType.SHIELD)

    @property
    def is_armor(self) -> bool:
        return any(t.is_armor for t in self.types)

    @property
    def is_shield(self) -> bool:
        return (
            ItemType.WEAPON in self.types and self.weapon_data.type == WeaponType.SHIELD
        )


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
        self.slot: ItemType | None = TYPE_MAP.get(data["Slot_0"])
        self.weight: ArmorWeight | None = ARMOR_WEIGHT_MAP.get(data["ArmorWeight_0"])
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
        self.speed: WeaponSpeed | None = SPEED_MAP.get(data["WeaponSpeed_0"])
        self.type: WeaponType | None = WEAPON_TYPE_MAP.get(data["WeaponType_0"])
        self.sharpness: Sharpness | None = SHARPNESS_MAP.get(data["Sharpness_0"])
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
        self.damage_type: DamageType | None = None
        if self.type == WeaponType.STAFF:
            self.damage_type = DamageType.TECHNOMANCY
        elif self.sharpness == Sharpness.SHARP:
            self.damage_type = DamageType.SHARP
        elif self.sharpness == Sharpness.BLUNT:
            self.damage_type = DamageType.BLUNT


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
