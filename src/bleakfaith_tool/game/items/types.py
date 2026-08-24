from enum import Enum


class ItemType(Enum):
    BLUEPRINT = "Blueprint"
    CONSUMABLE = "Consumable"
    AMULET = "Amulet"
    CAPE = "Cape"
    CHEST = "Chest"
    GLOVES = "Gloves"
    HELMET = "Helmet"
    LEGS = "Legs"
    RING = "Ring"
    SHOULDER = "Shoulder"
    WEAPON = "Weapon"
    FRAGMENT = "Fragment"
    MATERIAL = "Material"
    QUEST_ITEM = "Quest item"
    RESOURCE = "Resource"
    USABLE = "Usable"

    @property
    def is_armor(self) -> bool:
        return self in {
            ItemType.CHEST,
            ItemType.GLOVES,
            ItemType.HELMET,
            ItemType.LEGS,
            ItemType.SHOULDER,
        }

    @property
    def is_accessory(self) -> bool:
        return self in {ItemType.AMULET, ItemType.RING}

    @property
    def is_equipment(self) -> bool:
        return (
            self.is_armor
            or self.is_accessory
            or self == ItemType.WEAPON
            or self == ItemType.CAPE
        )


class WeaponSpeed(Enum):
    FAST = "Fast"
    SLOW = "Slow"
    SLUGGISH = "Sluggish"
    SWIFT = "Swift"


class WeaponType(Enum):
    CLAW = "Claw"
    CROSSBOW = "Crossbow"
    DUAL_BLADES = "Dual blades"
    DUAL_DAGGERS = "Dual daggers"
    DUAL_SICKLES = "Dual sickles"
    FANG = "Fang"
    GAUNTLET = "Gauntlet"
    GREAT_AXE = "Greataxe"
    GREAT_MACE = "Greatmace"
    GREAT_SWORD = "GreatSword"
    HALBERD = "Halberd"
    LONGBOW = "Longbow"
    ONE_HANDED_AXE = "One-handed axe"
    ONE_HANDED_LANCE = "One-handed lance"
    ONE_HANDED_MACE = "One-handed mace"
    ONE_HANDED_PICK = "One-handed pick"
    ONE_HANDED_STAFF = "One-handed staff"
    ONE_HANDED_SWORD = "One-handed sword"
    SHIELD = "Shield"
    SPEAR = "Spear"
    STAFF = "Staff"
    TAIL = "Tail"
    TORCH = "Torch"
    TWINBLADE = "Twinblade"
    TWO_HANDED_AXE = "Two-handed axe"
    TWO_HANDED_MACE = "Two-handed mace"
    TWO_HANDED_SCYTHE = "Two-handed scythe"
    TWO_HANDED_SWORD = "Two-handed sword"


class Sharpness(Enum):
    BLUNT = "Blunt"
    SHARP = "Sharp"


class DamageType(Enum):
    BLUNT = "Blunt"
    SHARP = "Sharp"
    TECHNOMANCY = "Technomancy"


class ArmorWeight(Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    CLOTH = "Cloth"
