from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GROUP, PRIVATE, Event, PrivateMessageEvent, GroupMessageEvent, MessageSegment
from typing import List
from .data_source import Cards, meanings, global_config

if not hasattr(global_config, "chain_reply"):
    CHAIN_REPLY = False
else:
    CHAIN_REPLY = global_config.chain_reply

if not hasattr(global_config, "nickname"):
    NICKNAME = "Bot"
    raise Exception("Bot'd better have a nickname maybe.")
else:
    _NICKNAME = global_config.nickname
    if len(list(_NICKNAME)) > 0:
        NICKNAME = list(_NICKNAME)[0]
    else:
        NICKNAME = "Bot"

__tarot_vsrsion__ = "v0.2.5"
plugin_notes = f'''
塔罗牌 {__tarot_vsrsion__}
[塔罗牌] 得到单张塔罗牌回应
[占卜]  全套占卜'''.strip()

plugin_help = on_command("塔罗牌帮助", permission=GROUP|PRIVATE, priority=6, block=True)
tarot = on_command("塔罗牌", permission=GROUP|PRIVATE, priority=6, block=True)
divine = on_command("占卜", permission=GROUP|PRIVATE, priority=6, block=True)

@plugin_help.handle()
async def show_help(bot: Bot, event: Event):
    await plugin_help.finish(plugin_notes)

@tarot.handle()
async def _(bot: Bot, event: Event):
    card = Cards(1)
    card_key, card_value, image_file = card.reveal()
    if isinstance(event, GroupMessageEvent): 
        msg = MessageSegment.text(f"\n回应是：{card_key}\n「{card_value}」\n") + MessageSegment.image(image_file)
        await tarot.finish(message=msg, at_sender=True)
    else:
        msg = MessageSegment.text(f"回应是：{card_key}\n「{card_value}」\n") + MessageSegment.image(image_file)
        await tarot.finish(message=msg, at_sender=False)

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
