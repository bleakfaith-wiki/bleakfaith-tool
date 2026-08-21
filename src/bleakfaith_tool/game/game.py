import os.path

import structlog

from bleakfaith_tool.game.l10n import Translations
from bleakfaith_tool.unreal import DataTable, EnumEntry, UserDefinedEnum
from bleakfaith_tool.unreal.assets import from_registry_file as assets_from_registry

LOG = structlog.get_logger()

BLOCKED_L10N = {"DT_LoadingScreen_Loc"}


class Game:
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        self.enums: dict[str, UserDefinedEnum] = {}
        self.data_tables: dict[str, DataTable] = {}
        self.translations = Translations()
        registry_path = os.path.join(base_path, "AssetRegistry.json")
        assets = assets_from_registry(registry_path)
        enum_paths = []
        data_table_paths = []
        for asset in assets:
            match asset.asset_class:
                case "DataTable":
                    data_table_paths.append(asset.package_name.lstrip("/") + ".json")
                case "UserDefinedEnum":
                    enum_paths.append(asset.package_name.lstrip("/") + ".json")
        self.load_enums(enum_paths, False)
        self.load_data_tables(data_table_paths, False)
        LOG.info(
            "loaded assets",
            enum_count=len(self.enums),
            data_table_count=len(self.data_tables),
        )

    def load_enum(self, path: str, strict: bool = True) -> None:
        path = os.path.join(self.base_path, path)
        if os.path.exists(path):
            enum = UserDefinedEnum.from_file(path)
            self.enums[enum.name] = enum
            LOG.debug("loaded enum", path=path)
        else:
            LOG.warning("enum file not found", path=path)
            if strict:
                raise FileNotFoundError(f"Enum file not found: {path}")

    def load_enums(self, paths: list[str], strict: bool = True) -> None:
        for path in paths:
            self.load_enum(path, strict)

    def load_data_table(self, path: str, strict: bool = True) -> None:
        path = os.path.join(self.base_path, path)
        if not os.path.exists(path):
            LOG.warning("data table file not found", path=path)
            if strict:
                raise FileNotFoundError(f"DataTable file not found: {path}")
            return

        data_table = DataTable.from_file(path)
        self.data_tables[data_table.name] = data_table
        LOG.debug("loaded data table", path=path)
        if (
            data_table.name not in BLOCKED_L10N
            and data_table.name.startswith("DT_")
            and data_table.name.endswith("_Loc")
        ):
            self.load_l10n(data_table.name)

    def load_data_tables(self, paths: list[str], strict: bool = True) -> None:
        for path in paths:
            self.load_data_table(path, strict)

    def load_l10n(self, *names: str) -> None:
        for name in names:
            data_table = self.data_table(name)
            self.translations.add_from_data_table(data_table)
            LOG.debug("loaded localization", name=name)

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
