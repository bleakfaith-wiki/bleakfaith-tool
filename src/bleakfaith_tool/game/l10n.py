from bleakfaith_tool.unreal import DataTable


class Translations:
    def __init__(self) -> None:
        self.strings = {}

    def __call__(self, key: str, default: str | None = None) -> str:
        return self.get(key, default)

    def get(self, key: str, default: str | None = None) -> str:
        return self.strings.get(key, default or key)

    def add_from_data_table(self, data_table: DataTable) -> None:
        for key, row in data_table.rows.items():
            l10n_list = next(v for k, v in row.items() if "Localization_" in k)
            value = next(
                e["Value"] for e in l10n_list if e["Key"] == "Languages::NewEnumerator1"
            )
            if value:
                if key in self.strings:
                    raise ValueError(f"Duplicate translation key: {key}")
                self.strings[key] = value
