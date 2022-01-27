import nonebot
from typing import List
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, GroupMessageEvent, MessageSegment
from .data_source import Cards, meanings

CHAIN_REPLY = nonebot.get_driver().config.chain_reply
_NICKNAME = nonebot.get_driver().config.nickname
NICKNAME = "awesome_bot" if not _NICKNAME else list(_NICKNAME)[0]

tarot = on_command("塔罗牌", priority=5, block=True)
divine = on_command("占卜", priority=5, block=True)

@tarot.handle()
async def _(bot: Bot, event: Event):
    card = Cards(1)
    card_key, card_value, image_file = card.reveal()
    msg = MessageSegment.text(f"回应是：{card_key}\n「{card_value}」\n") + MessageSegment.image(image_file)
    if isinstance(event, GroupMessageEvent): 
        await tarot.finish(message=msg, at_sender=True)
    else:
        await tarot.finish(message=msg)

@divine.handle()
async def _(bot: Bot, event: Event):
    await divine.send("请稍等，正在洗牌中")
    cards = Cards(4)
    chain = []
    for count in range(4):
        card_key, card_value, image_file = cards.reveal()
        meaning_key = list(meanings.keys())[count]
        meaning_value = meanings[meaning_key]

        if isinstance(event, PrivateMessageEvent):
            text = meaning_key + "，" + meaning_value + "\n" + card_key + "，" + card_value + "\n"
            msg = MessageSegment.text(text)+ MessageSegment.image(image_file)
            if count < 3:
                await bot.send_private_msg(user_id=event.user_id, message=msg)
            else:
                await bot.send_private_msg(user_id=event.user_id, message=msg)

        if isinstance(event, GroupMessageEvent):
            if not CHAIN_REPLY:           
                text = meaning_key + "，" + meaning_value + "\n" + card_key + "，" + card_value + "\n"
                msg = MessageSegment.text(text) + MessageSegment.image(image_file)
                if count < 3:
                    await bot.send(event=event, message=msg, at_sender=True)
                else:
                    await divine.finish(message=msg, at_sender=True)
            else:
                text = meaning_key + "，" + meaning_value + "\n" + card_key + "，" + card_value + "\n"
                msg = MessageSegment.text(text) + MessageSegment.image(image_file)
                if count < 4:
                    chain = await chain_reply(bot, chain, msg)
            if CHAIN_REPLY and count == 3:
                await bot.send_group_forward_msg(group_id=event.group_id, messages=chain)

async def chain_reply(bot: Bot, chain: List, msg: MessageSegment) -> List:
    data = {
        "type": "node",
        "data": {
            "name": f"{NICKNAME}",
            "uin": f"{bot.self_id}",
            "content": msg
        },
    }
    chain.append(data)
    return chain
