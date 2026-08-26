import logging
import os
import sys

import structlog

from bleakfaith_tool.game import Game
from bleakfaith_tool.game.abilities import abilities_from_data_table
from bleakfaith_tool.game.fragments import fragments_from_data_table
from bleakfaith_tool.game.items import Items
from bleakfaith_tool.game.loot_table import loot_tables_from_data_table
from bleakfaith_tool.game.npc import Npc
from bleakfaith_tool.game.recipes import recipes_from_game
from bleakfaith_tool.gen import LuaGenerator

LOG = structlog.get_logger()


def env_or_raise(name: str) -> str:
    if value := os.getenv(name):
        return value
    LOG.error("environment variable not set", name=name)
    raise RuntimeError(f"Environment variable {name} is not set.")


def update_wiki(data: dict[str, str]) -> None:
    from bleakfaith_tool.wiki import get_modifier

    modifier = get_modifier(data)
    modifier.run()


def main() -> int:
    log_level = os.getenv("LOG_LEVEL")
    if log_level:
        log_level = log_level.upper()
    else:
        log_level = logging.INFO

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(),
        ],
    )

    LOG.info("Starting")

    export_path = env_or_raise("BFF_EXPORT_PATH")

    game = Game(export_path)

    guid_path = env_or_raise("BFF_GUID_PATH")

    recipes = recipes_from_game(game)
    items = Items(guid_path, game.translations)

    loot_tables_dt = game.data_table("DT_ItemSets")
    loot_tables = loot_tables_from_data_table(loot_tables_dt)

    fragments_dt = game.data_table("DT_Fragment")
    fragments = fragments_from_data_table(fragments_dt, game)

    ability_fragments_by_path = {
        f.ability_data.asset_path_name[: f.ability_data.asset_path_name.rfind(".")]: f
        for f in fragments.values()
        if f.ability_data is not None
    }

    ability_dt = game.data_table("DT_Abilities")
    abilities = abilities_from_data_table(ability_dt, game, ability_fragments_by_path)

    npcs = [
        Npc.from_bpgc(bp, name, game.translations)
        for name, bp in game.bpgcs.items()
        if name.startswith("NPC_") or "_DocileNPC_" in name
    ]

    luagen = LuaGenerator("out/lua")

    wikidata = {
        "Module:GameData/items": luagen.write_items(items),
        "Module:GameData/weapons": luagen.write_weapons(items, fragments, abilities),
        "Module:GameData/armor": luagen.write_armor(items),
        "Module:GameData/shields": luagen.write_shields(items, fragments, abilities),
        "Module:GameData/lootTables": luagen.write_loot_tables(loot_tables, items),
        "Module:GameData/abilities": luagen.write_abilities(abilities),
        "Module:GameData/fragments": luagen.write_fragments(fragments),
        "Module:GameData/recipes": luagen.write_recipes(recipes, items),
        "Module:GameData/npcs": luagen.write_npcs(npcs, items, loot_tables),
    }

    if "--update" in sys.argv:
        update_wiki(wikidata)

    return 0


if __name__ == "__main__":
    sys.exit(main())
