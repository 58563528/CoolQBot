import json
from pathlib import Path

import pytest
from nonebug import App
from pytest_mock import MockerFixture

from tests.fake import fake_group_message_event


def mocked_get(url: str, **kwargs):
    class MockResponse:
        def __init__(self, json: dict):
            self._json = json

        def json(self):
            return self._json

    test_dir = Path(__file__).parent
    if url == "http://netease:3000/search?keywords=test":
        with open(test_dir / "netease.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return MockResponse(data)

    return MockResponse({})


@pytest.mark.asyncio
@pytest.mark.parametrize("app", [("src.plugins.music",)], indirect=True)
async def test_music(
    app: App,
    mocker: MockerFixture,
):
    """测试音乐"""
    from nonebot import get_driver
    from nonebot.adapters.onebot.v11 import Adapter, Bot, Message, MessageSegment
    from nonebug.mixin.call_api.fake import make_fake_adapter, make_fake_bot

    from src.plugins.music import music_cmd

    get = mocker.patch("httpx.AsyncClient.get", side_effect=mocked_get)

    async with app.test_matcher(music_cmd) as ctx:
        adapter = make_fake_adapter(Adapter)(get_driver(), ctx)
        bot = make_fake_bot(Bot)(adapter, "1")
        event = fake_group_message_event(message=Message("/music test"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, MessageSegment.music("163", 1825190456), "result")
        ctx.should_finished()

    get.assert_called_once_with("http://netease:3000/search?keywords=test")


@pytest.mark.asyncio
@pytest.mark.parametrize("app", [("src.plugins.music",)], indirect=True)
async def test_music_get_arg(
    app: App,
    mocker: MockerFixture,
):
    """测试启动问候已开启的情况"""
    from nonebot import get_driver
    from nonebot.adapters.onebot.v11 import Adapter, Bot, Message, MessageSegment
    from nonebug.mixin.call_api.fake import make_fake_adapter, make_fake_bot

    from src.plugins.music import music_cmd

    get = mocker.patch("httpx.AsyncClient.get", side_effect=mocked_get)

    async with app.test_matcher(music_cmd) as ctx:
        adapter = make_fake_adapter(Adapter)(get_driver(), ctx)
        bot = make_fake_bot(Bot)(adapter, "1")
        event = fake_group_message_event(message=Message("/music"))
        next_event = fake_group_message_event(message=MessageSegment.image("12"))
        final_event = fake_group_message_event(message=Message("test"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "你想听哪首歌呢？", "result")
        ctx.should_rejected()
        ctx.receive_event(bot, next_event)
        ctx.should_call_send(next_event, "歌曲名不能为空呢，请重新输入！", "result")
        ctx.should_rejected()
        ctx.receive_event(bot, final_event)
        ctx.should_call_send(
            final_event, MessageSegment.music("163", 1825190456), "result"
        )
        ctx.should_finished()

    get.assert_called_once_with("http://netease:3000/search?keywords=test")