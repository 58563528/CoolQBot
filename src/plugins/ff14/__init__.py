"""最终幻想XIV"""

from pathlib import Path

import nonebot
from nonebot import CommandGroup, get_driver, require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_datastore")
require("nonebot_plugin_user")

__plugin_meta__ = PluginMetadata(
    name="最终幻想XIV",
    description="与最终幻想XIV有关的功能",
    usage="与最终幻想XIV有关的功能",
)

ff14 = CommandGroup("ff14", block=True)

global_config = get_driver().config

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "plugins").resolve()))
