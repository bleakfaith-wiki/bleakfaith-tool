import json
from dataclasses import dataclass


def make_package_flags(data: dict | None) -> list[str]:
    if data is None:
        return []

    flags: str | None = data.get("PackageFlags", None)
    if flags is None:
        return []

    return [flag.strip() for flag in flags.split("|")]


def from_registry_file(path: str) -> list[Asset]:
    with open(path, "r") as f:
        registry = json.load(f)

    if asset_entries := registry.get("PreallocatedAssetDataBuffers"):
        return [Asset.from_data(entry) for entry in asset_entries]

    return []


@dataclass
class Asset:
    object_path: str
    package_name: str
    package_path: str
    asset_name: str
    asset_class: str
    tags: dict[str, str]
    chunk_ids: list[int]
    package_flags: list[str]

    @staticmethod
    def from_data(data: dict) -> Asset:
        return Asset(
            data["ObjectPath"],
            data["PackageName"],
            data["PackagePath"],
            data["AssetName"],
            data["AssetClass"],
            data.get("TagsAndValues", {}),
            data.get("ChunkIDs", []),
            make_package_flags(data),
        )
