"""每日早安插件"""

from pathlib import Path

import nonebot
from nonebot import get_driver, get_plugin_config, require
from nonebot.plugin import PluginMetadata

from .config import Config

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_datastore")
require("nonebot_plugin_saa")
require("nonebot_plugin_user")

__plugin_meta__ = PluginMetadata(
    name="问好",
    description="早上好下午好晚上好",
    usage="",
    supported_adapters={"~onebot.v11"},
)

_sub_plugins = set()

global_config = get_driver().config
plugin_config = get_plugin_config(Config)

_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "plugins").resolve()))
