import json


class UserDefinedEnum:
    def __init__(self, data: dict) -> None:
        self.type: str = data["Type"]
        self.name: str = data["Name"]
        self.klass: str = data["Class"]
        self.package: str = data["Package"]
        self.entries: list[EnumEntry] = []
        self.by_name: dict[str, EnumEntry] = {}
        self.by_key: dict[str, EnumEntry] = {}
        self.by_value: dict[int, EnumEntry] = {}
        names = data["Names"]
        max_name = max(names, key=names.get)
        if max_name[-4:] != "_MAX":
            max_name = None
        self.max: int | None = names[max_name] if max_name else None

        for dn_data in data["Properties"]["DisplayNameMap"]:
            key = dn_data["Key"]
            name = f"{self.name}::{key}"
            value = names[name]
            display = EnumEntryDisplayName(
                dn_data["Value"]["SourceString"], dn_data["Value"]["LocalizedString"]
            )
            entry = EnumEntry(name, key, value, display)
            self.entries.append(entry)
            self.by_name[name] = entry
            self.by_key[key] = entry
            self.by_value[value] = entry

    @staticmethod
    def from_file(path: str) -> UserDefinedEnum:
        with open(path, "r") as f:
            data = json.load(f)[0]
        return UserDefinedEnum(data)


class EnumEntry:
    def __init__(
        self, name: str, key: str, value: int, display: EnumEntryDisplayName
    ) -> None:
        self.name = name
        self.key = key
        self.value = value
        self.display = display


class EnumEntryDisplayName:
    def __init__(self, source: str, localized: str) -> None:
        self.source = source
        self.localized = localized

    def __str__(self) -> str:
        return self.source
