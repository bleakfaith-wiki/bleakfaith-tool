import os
import sys

import structlog

from bleakfaith_tool.game import Game
from bleakfaith_tool.game.items import load_from_guid_file as load_items_from_guid_file
from bleakfaith_tool.game.loot_table import loot_tables_from_data_table
from bleakfaith_tool.game.recipes import recipes_from_game

LOG = structlog.get_logger()


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

    export_path = os.getenv("BFF_EXPORT_PATH")
    if export_path is None:
        LOG.error("BFF_EXPORT_PATH environment variable is not set.")
        return 1

    game = Game(export_path)

    guid_path = os.getenv("BFF_GUID_PATH")

    if guid_path is None:
        LOG.error("BFF_GUID_PATH environment variable is not set.")
        return 1

    recipes = recipes_from_game(game)
    inv_data = load_items_from_guid_file(guid_path, game)

    loot_tables_dt = game.data_table("DT_ItemSets")
    loot_tables = loot_tables_from_data_table(loot_tables_dt)

    lt_evolved_plagued = [lt for lt in loot_tables.values() if lt.id in (1, 4, 30)]

    for lt in lt_evolved_plagued:
        print(f"Loot table {lt.note}:")
        for entry in lt.entries:
            item = next(i for i in inv_data.values() if i.id == entry.item_id)
            print(
                f"  {entry.rate * 100}% of {entry.min}-{entry.max}x {item.name} (id={entry.item_id})"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
