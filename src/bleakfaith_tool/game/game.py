import os.path

import structlog

from bleakfaith_tool.game.data_tables import DATA_TABLE_PATHS
from bleakfaith_tool.game.enums import ENUM_PATHS
from bleakfaith_tool.game.l10n import Translations
from bleakfaith_tool.unreal import DataTable, EnumEntry, UserDefinedEnum

LOG = structlog.get_logger()

BLOCKED_L10N = {"DT_LoadingScreen_Loc"}


class Game:
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        self.enums: dict[str, UserDefinedEnum] = {}
        self.data_tables: dict[str, DataTable] = {}
        self.translations = Translations()
        self.load_enums(ENUM_PATHS)
        self.load_data_tables(DATA_TABLE_PATHS)

    def load_enum(self, path: str) -> None:
        LOG.debug("loading enum", path=path)
        path = os.path.join(self.base_path, path)
        enum = UserDefinedEnum.from_file(path)
        self.enums[enum.name] = enum

    def load_enums(self, paths: list[str]) -> None:
        for path in paths:
            self.load_enum(path)

    def load_data_table(self, path: str) -> None:
        LOG.debug("loading data table", path=path)
        path = os.path.join(self.base_path, path)
        data_table = DataTable.from_file(path)
        self.data_tables[data_table.name] = data_table
        if (
            data_table.name not in BLOCKED_L10N
            and data_table.name.startswith("DT_")
            and data_table.name.endswith("_Loc")
        ):
            self.load_l10n(data_table.name)

    def load_data_tables(self, paths: list[str]) -> None:
        for path in paths:
            self.load_data_table(path)

    def load_l10n(self, *names: str) -> None:
        for name in names:
            LOG.debug("loading localization", name=name)
            data_table = self.data_table(name)
            self.translations.add_from_data_table(data_table)

    def enum(self, name: str) -> UserDefinedEnum:
        enum = self.enums.get(name)
        if enum:
            return enum
        raise ValueError(f"Enum '{name}' not found in loaded enums.")

    def enum_entry(self, name: str) -> EnumEntry | None:
        enum_name = name.split("::")[0]
        enum = self.enum(enum_name)
        if enum is None:
            return None
        return enum.by_name.get(name)

    def enum_display(self, name: str) -> str | None:
        entry = self.enum_entry(name)
        if entry is None:
            return None
        return entry.display.source

    def data_table(self, name: str) -> DataTable:
        data_table = self.data_tables.get(name)
        if data_table:
            return data_table
        raise ValueError(f"DataTable '{name}' not found in loaded data tables.")

    def translate(self, key: str, default: str | None = None) -> str:
        return self.translations.get(key, default)
