import os
import sys

import structlog

from bleakfaith_tool.game import Game
from bleakfaith_tool.game.items import Items
from bleakfaith_tool.game.loot_table import loot_tables_from_data_table
from bleakfaith_tool.game.recipes import recipes_from_game
from bleakfaith_tool.gen import LuaGenerator

LOG = structlog.get_logger()


def env_or_raise(name: str) -> str:
    if value := os.getenv(name):
        return value
    LOG.error("environment variable not set", name=name)
    raise RuntimeError(f"Environment variable {name} is not set.")


def main() -> int:
    structlog.configure(
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
        ]
    )

    LOG.info("Starting")

    export_path = env_or_raise("BFF_EXPORT_PATH")

    game = Game(export_path)

    guid_path = env_or_raise("BFF_GUID_PATH")

    recipes = recipes_from_game(game)
    items = Items(guid_path, game.translations)

    loot_tables_dt = game.data_table("DT_ItemSets")
    loot_tables = loot_tables_from_data_table(loot_tables_dt)

    lt_evolved_plagued = [lt for lt in loot_tables.values() if lt.id in (1, 4, 30, 43)]

    # for lt in lt_evolved_plagued:
    #     print(f"Loot table {lt.note}:")
    #     for entry in lt.entries:
    #         item = items.id_first(entry.item_id)
    #         print(
    #             f"  {entry.rate * 100}% of {entry.min}-{entry.max}x {item.name} (id={entry.item_id})"  # ty: ignore[unresolved-attribute]
    #         )

    luagen = LuaGenerator("out/lua")

    luagen.write_items(items)
    luagen.write_weapons(items)
    luagen.write_loot_tables(loot_tables, items)

    return 0


if __name__ == "__main__":
    sys.exit(main())
