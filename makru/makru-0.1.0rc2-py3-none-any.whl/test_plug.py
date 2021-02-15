import pytest
from pathlib import Path
from . import plug


class TestPlugBox:
    def get_self_plugbox(self):
        p = Path(".") / "tools" / "plugins"
        if p.exists():
            box = plug.PlugBox()
            box.searchpaths.append(p)
            return box

    def test_can_create_plugbox(self):
        plug.PlugBox()

    def test_can_find_plugin_correctly(self):
        PLUGNAME = "empty-plugin"
        box = self.get_self_plugbox()
        if box:
            box.exists(PLUGNAME)
        else:
            pytest.skip("could not find correct plugin folder for test")
