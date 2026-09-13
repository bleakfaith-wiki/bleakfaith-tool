import json
from dataclasses import dataclass

from bleakfaith_tool.game.l10n import Translations
from bleakfaith_tool.unreal import BlueprintGeneratedClass


class Npc:
    def __init__(
        self, blueprint: BlueprintGeneratedClass, asset_name: str, l10n: Translations
    ) -> None:
        bp_data = blueprint.data
        bp_entry = next(e for e in bp_data if e["Type"] == "BlueprintGeneratedClass")
        npc = next(e for e in bp_data if e["Type"] == bp_entry["Name"])
        combat = next((e for e in bp_data if e["Type"] == "BP_CombatComponent_C"), None)
        equipment = next(
            (e for e in bp_data if e["Type"] == "BP_EquipmentComponent_C"), None
        )
        stats = next((e for e in bp_data if e["Type"] == "BP_StatComponent_C"), None)

        self.id: str = asset_name
        self.loot_tables: list[int] = []
        self.extra_loot: list[int] = []
        self.can_ragdoll: bool | None = None
        self.should_ragdoll: bool | None = None
        self.faithful_stacks: int | None = None
        self.max_perfect_block_counter: int | None = None
        self.perfect_block_reset_timer: float | None = None
        self.equipped_items: list[int] = []
        self.is_boss: bool | None = None
        self.is_undamageable: bool | None = None
        self.attributes: Attributes | None = None
        self.capabilities: list[NpcCapability] = []
        self.experience: dict[int, int] = {}

        if props := npc.get("Properties"):
            if el := props.get("ExtraLoot"):
                self.extra_loot = el
            if lis := props.get("LootItemSets"):
                self.loot_tables = sorted(lis)
            self.can_ragdoll = props.get("CanRagdoll?")
            self.should_ragdoll = props.get("ShouldRagdoll")
            self.faithful_stacks = props.get("FaithfulStacks")

        if combat:
            props = combat["Properties"]
            self.max_perfect_block_counter = props.get("MaxPerfectBlockCounter")
            self.perfect_block_reset_timer = props.get("PerfectBlockResetTimer")

        if equipment:
            props = equipment["Properties"]
            if el := props.get("EquippedItems"):
                self.equipped_items = [id for id in el if id != -1]

        if stats and (props := stats.get("Properties")):
            self.is_boss = props.get("Boss")
            self.is_undamageable = props.get("Undamageable")
            if exp_curve := props.get("ExperienceCurve"):
                self.experience = {int(e["Key"]): e["Value"] for e in exp_curve}

            if starting := props.get("StartingSkills"):
                for key, entry in starting.items():
                    if key.startswith("Attributes_"):
                        self.attributes = Attributes.from_list(entry, l10n)
                    elif key.startswith("Capabilities_"):
                        for e in entry:
                            k = e["Key"]
                            v: dict[str, float] = e["Value"]
                            for v_k, v_v in v.items():
                                if v_k.startswith("CurrentValue"):
                                    current = v_v
                                elif v_k.startswith("SoftCap"):
                                    soft_cap = v_v
                                elif v_k.startswith("HardCap"):
                                    hard_cap = v_v
                            self.capabilities.append(
                                NpcCapability(
                                    key=l10n(k),
                                    current=current,
                                    soft_cap=soft_cap,
                                    hard_cap=hard_cap,
                                )
                            )

    @staticmethod
    def from_bpgc(
        bpgc: BlueprintGeneratedClass, asset_name: str, l10n: Translations
    ) -> Npc:
        return Npc(bpgc, asset_name, l10n)

    @staticmethod
    def from_file(path: str, asset_name: str, l10n: Translations) -> Npc:
        with open(path, "r") as f:
            blueprint_data: list[dict] = json.load(f)
        blueprint = BlueprintGeneratedClass("inline", path, blueprint_data)
        return Npc.from_bpgc(blueprint, asset_name, l10n)


@dataclass
class Attributes:
    strength: int | None
    agility: int | None
    constitution: int | None
    intelligence: int | None

    @staticmethod
    def from_list(data: list[dict[str, str | int]], l10n: Translations) -> Attributes:
        for entry in data:
            key = l10n(entry["Key"])  # ty: ignore[invalid-argument-type]
            value: int = entry["Value"]  # ty: ignore[invalid-assignment]
            strength: int | None = None
            agility: int | None = None
            constitution: int | None = None
            intelligence: int | None = None
            match key:
                case "Strength":
                    strength = value
                case "Agility":
                    agility = value
                case "Constitution":
                    constitution = value
                case "Intelligence":
                    intelligence = value
        return Attributes(
            strength=strength,
            agility=agility,
            constitution=constitution,
            intelligence=intelligence,
        )


@dataclass
class NpcCapability:
    key: str
    current: float
    soft_cap: float
    hard_cap: float
