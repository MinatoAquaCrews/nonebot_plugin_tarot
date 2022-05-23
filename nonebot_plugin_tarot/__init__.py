from nonebot import on_command, on_regex
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, PrivateMessageEvent, GroupMessageEvent
from typing import List, Dict, Union
from .config import tarot_config
from .data_source import tarot_manager

__tarot_version__ = "v0.3.0"
__tarot_notes__ = f'''
塔罗牌 {__tarot_version__}
[占卜/塔罗牌] 随机选取牌阵进行占卜
[开启/启用/关闭/禁用]群聊转发 开启或关闭全局群聊转发'''.strip()

tarot = on_command(cmd="占卜", aliases={"塔罗牌"}, priority=7)
chain_reply_switch = on_regex(pattern=r"(开启|启用|关闭|禁用)群聊转发", permission=SUPERUSER, priority=7, block=True)

@tarot.handle()
async def _(bot: Bot, event: MessageEvent):
    # 发送牌阵
    msg, cards_num = await tarot_manager.divine()
    await tarot.send(msg)
    
    chain = []
    for i in range(cards_num):
        reveal_msg = await tarot_manager.reveal(i)

        if isinstance(event, PrivateMessageEvent):
            if i < cards_num:
                await tarot.send(reveal_msg)
            else:
                await tarot.finish(reveal_msg)

        if isinstance(event, GroupMessageEvent):
            if not tarot_manager.is_chain_reply:
                # 开启群聊转发模式
                if i < cards_num - 1:
                    await tarot.send(reveal_msg)
                else:
                    await tarot.finish(reveal_msg)
            else:
                chain = await chain_reply(bot, chain, reveal_msg)
            
    if tarot_manager.is_chain_reply:
        await bot.send_group_forward_msg(group_id=event.group_id, messages=chain)

@chain_reply_switch.handle()
async def _(event: GroupMessageEvent):
    args = event.get_plaintext()
    msg = []
    if args[:2] == "开启" or args[:2] == "启用":
        tarot_manager.switch_chain_reply(True)
        msg = "占卜群聊转发模式已开启~"
    elif args[:2] == "关闭" or args[:2] == "禁用":
        tarot_manager.switch_chain_reply(False)
        msg = "占卜群聊转发模式已关闭~"
    
    await chain_reply_switch.finish(msg)

async def chain_reply(bot: Bot, chain: List[Dict[str, Union[str, Dict[str, Union[str, MessageSegment]]]]], msg: MessageSegment) -> List[Dict[str, Union[str, Dict[str, Union[str, MessageSegment]]]]]:
    data = {
        "type": "node",
        "data": {
            "name": f"{list(tarot_config.nickname)[0]}",
            "uin": f"{bot.self_id}",
            "content": msg
        },
    }
    chain.append(data)
    return chain