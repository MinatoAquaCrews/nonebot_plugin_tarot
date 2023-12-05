from nonebot import on_command, on_regex, require
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import (
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_localstore")  # isort:skip

from .config import PluginConfig
from .data_source import tarot_manager

__plugin_version__ = "v0.5.0a3"
__plugin_usages__ = f"""
塔罗牌 {__plugin_version__}
[占卜] 随机选取牌阵进行占卜
[塔罗牌] 得到单张塔罗牌回应
[开启/启用/关闭/禁用]群聊转发 开启或关闭全局群聊转发""".strip()

__plugin_meta__ = PluginMetadata(
    name="塔罗牌",
    description="塔罗牌！魔法占卜🔮",
    usage=__plugin_usages__,
    type="application",
    homepage="https://github.com/MinatoAquaCrews/nonebot_plugin_tarot",
    config=PluginConfig,
    extra={
        "author": "KafCoppelia <k740677208@gmail.com>",
        "version": __plugin_version__,
    },
    supported_adapters={"~onebot.v11"},
)

divine = on_command(cmd="占卜", priority=7)
tarot = on_command(cmd="塔罗牌", priority=7)
chain_reply_switch = on_regex(
    pattern=r"^(开启|启用|关闭|禁用)群聊转发(模式)?$", permission=SUPERUSER, priority=7, block=True
)


@divine.handle()
async def general_divine_in_group(
    bot: Bot, matcher: Matcher, event: GroupMessageEvent
) -> None:
    arg = event.get_plaintext()

    if "帮助" in arg[-2:]:
        await matcher.finish(__plugin_usages__)

    await tarot_manager.divine_in_group(bot, matcher, event.group_id)


@divine.handle()
async def general_divine_in_private(
    matcher: Matcher, event: PrivateMessageEvent
) -> None:
    arg = event.get_plaintext()

    if "帮助" in arg[-2:]:
        await matcher.finish(__plugin_usages__)

    await tarot_manager.divine_in_private(matcher)


@tarot.handle()
async def _(matcher: Matcher, event: MessageEvent):
    arg = event.get_plaintext()

    if "帮助" in arg[-2:]:
        await matcher.finish(__plugin_usages__)

    msg = await tarot_manager.get_one_tarot()
    await matcher.finish(msg)


@chain_reply_switch.handle()
async def _(event: GroupMessageEvent):
    arg = event.get_plaintext()
    base = "占卜群聊转发模式已{0}~"

    if arg[:2] == "开启" or arg[:2] == "启用":
        tarot_manager.is_chain_reply = True
        msg = base.format("开启")
    else:
        tarot_manager.is_chain_reply = False
        msg = base.format("关闭")

    await chain_reply_switch.finish(msg)
