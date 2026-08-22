import re


def normalize(path: str) -> str:
    """
    Normalize Unreal Engine paths to a consistent format.

    Depending on what tool was used to extract game assets, the paths may look different.
    UE Viewer (umodel) will use a path that starts with `/Game/`,
    while FModel will use `/Forsaken/Content/`.

    This function normalizes paths to use the style from UE Viewer.
    """
    return re.sub(r"^(/)?Forsaken/Content(/|$)", r"\1Game\2", path)
