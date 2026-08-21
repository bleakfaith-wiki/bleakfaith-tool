import os
import sys

import structlog

from bleakfaith_tool.game import Game
from bleakfaith_tool.game.items import load_from_guid_file as load_items_from_guid_file
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
