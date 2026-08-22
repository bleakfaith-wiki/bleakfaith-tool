import pytest

from bleakfaith_tool.unreal import paths


def test_subs_fmodel_prefix():
    assert paths.normalize("/Forsaken/Content/Some/Path") == "/Game/Some/Path"
    assert paths.normalize("Forsaken/Content/Some/Path") == "Game/Some/Path"


def test_doesnt_sub_umodel_prefix():
    assert paths.normalize("/Game/Some/Path") == "/Game/Some/Path"
    assert paths.normalize("Game/Some/Path") == "Game/Some/Path"


def test_subs_fmodel_prefix_when_str_ends_with_slash():
    assert paths.normalize("/Forsaken/Content/") == "/Game/"
    assert paths.normalize("Forsaken/Content/") == "Game/"


def test_subs_fmodel_prefix_when_str_ends_without_slash():
    assert paths.normalize("/Forsaken/Content") == "/Game"
    assert paths.normalize("Forsaken/Content") == "Game"


def test_doesnt_sub_when_str_continues_without_slash():
    assert paths.normalize("/Forsaken/ContentSome/Path") == "/Forsaken/ContentSome/Path"
    assert paths.normalize("Forsaken/ContentSome/Path") == "Forsaken/ContentSome/Path"
