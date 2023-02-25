import random
from pathlib import Path
from typing import List, Dict, Union, Tuple
from PIL import Image
from io import BytesIO
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent, PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Bot
from nonebot.matcher import Matcher
from .config import tarot_config, get_tarot
try:
    import ujson as json
except ModuleNotFoundError:
    import json


def chain_reply(bot: Bot, chain: List[Dict[str, Union[str, Dict[str, Union[str, MessageSegment]]]]], msg: MessageSegment) -> List[Dict[str, Union[str, Dict[str, Union[str, MessageSegment]]]]]:
    data = {
        "type": "node",
        "data": {
            "name": list(tarot_config.nickname)[0],
            "uin": bot.self_id,
            "content": msg
        },
    }
    chain.append(data)
    return chain


def pick_theme() -> str:
    themes: List[str] = [
        f.name for f in tarot_config.tarot_path.iterdir() if f.is_dir()]

    return random.choice(themes)


class Tarot:
    def __init__(self):
        self.tarot_json: Path = Path(__file__).parent / "tarot.json"
        self.is_chain_reply: bool = tarot_config.chain_reply

    async def divine(self, bot: Bot, matcher: Matcher, event: MessageEvent) -> None:
        '''
            Random choose a formation, return the formation dictionary
        '''
        with open(self.tarot_json, 'r', encoding='utf-8') as f:
            content = json.load(f)
            all_formations = content.get("formations")
            all_cards = content.get("cards")
            formation_name = random.choice(list(all_formations))
            formation = all_formations.get(formation_name)

        await matcher.send(f"启用{formation_name}，正在洗牌中")

        '''
            Get the number of cards to select & a list of cards
        '''
        cards_num: int = formation.get("cards_num")
        devined: List[str] = random.sample(list(all_cards), cards_num)
        is_cut: bool = formation.get("is_cut")
        represent: List[Union[str, List[str]]] = random.choice(
            formation.get("represent"))

        chain = []
        for i in range(cards_num):
            # Select the #i tarot
            card_info = all_cards.get(devined[i])
            if is_cut and i == cards_num - 1:
                msg_header = MessageSegment.text(f"切牌「{represent[i]}」\n")
            else:
                msg_header = MessageSegment.text(f"第{i+1}张牌「{represent[i]}」\n")

            flag, msg_body = await self._get_text_and_image(card_info)
            if not flag:
                await matcher.finish(msg_body)

            if isinstance(event, PrivateMessageEvent):
                if i < cards_num:
                    await matcher.send(msg_header + msg_body)
                else:
                    await matcher.finish(msg_header + msg_body)

            elif isinstance(event, GroupMessageEvent):
                if self.is_chain_reply:
                    chain = chain_reply(bot, chain, msg_header + msg_body)
                else:
                    if i < cards_num - 1:
                        await matcher.send(msg_header + msg_body)
                    else:
                        await matcher.finish(msg_header + msg_body)
            else:
                return None

        if self.is_chain_reply:
            await bot.send_group_forward_msg(group_id=event.group_id, messages=chain)

    async def single_divine(self) -> MessageSegment:
        '''
            Single divine, get a tarot
        '''
        # 1. Pick a theme randomly
        theme: str = pick_theme()

        card_info = self._get_card_info()

        msg: str = "回应是"
        flag, body = await self._get_text_and_image(card_info)

        if not flag:
            return body

        return msg + body

    def switch_chain_reply(self, new_state: bool) -> None:
        '''
            开启/关闭全局群聊转发模式
        '''
        self.is_chain_reply = new_state
    
    def _get_card_info(self, _theme: str) -> Dict[str, Union[str, Dict[str, str]]]:
        with open(self.tarot_json, 'r', encoding='utf-8') as f:
            content = json.load(f)
            all_cards = content.get("cards")
            
        if "Touhou" in _theme:
            only_MajorArcana = {
                k: v for k, v in all_cards.items() if int(k) < 22
            }
            card_index = random.choice(list(only_MajorArcana))
        else:
            card_index = random.choice(list(all_cards))
        
        card_info = all_cards.get(card_index)
        
        return card_info

    async def _get_text_and_image(self, card_info: Dict[str, Union[str, Dict[str, str]]]) -> Tuple[bool, MessageSegment]:
        '''
            Get a tarot image(up or down) & text arrcording to the card info
        '''

        # 2. Get or download the image
        name_cn: str = card_info.get("name_cn")
        img_path = Path(tarot_config.tarot_path / theme /
                        card_info.get("type")).glob(card_info.get("pic") + ".*")

        if not img_path.exists():
            data = await get_tarot(theme, card_info.get("type"), card_info.get("pic"))
            if data is None:
                return False, MessageSegment.text("图片下载出错，请重试……")

            img: Image.Image = Image.open(BytesIO(data))
        else:
            img: Image.Image = Image.open(img_path)

        # 3. Choose up or down
        if random.random() < 0.5:
            # 正位
            meaning = card_info.get("meaning").get("up")
            msg = MessageSegment.text(f"「{name_cn}正位」「{meaning}」\n")
        else:
            meaning = card_info.get("meaning").get("down")
            msg = MessageSegment.text(f"「{name_cn}逆位」「{meaning}」\n")
            img = img.rotate(180)

        buf = BytesIO()
        img.save(buf, format='png')

        return True, msg + MessageSegment.image(buf)


tarot_manager = Tarot()
