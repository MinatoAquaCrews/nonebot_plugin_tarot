import random
from pathlib import Path 
from typing import List, Dict, Union, Tuple
from PIL import Image
from io import BytesIO
from nonebot.adapters.onebot.v11 import MessageSegment
from .config import tarot_config
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class Tarot:
    def __init__(self):
        self.tarot_json: Path = tarot_config.tarot_path / "tarot.json"
        with open(self.tarot_json, 'r', encoding='utf-8') as f:
            _formations = json.load(f).get("formation")
            _cards = json.load(f).get("cards")
            
        self._formations: Dict[str, Dict[str, Union[int, bool, List[List[str]]]]] = _formations
        self._cards: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = _cards
        self.cards_num: int = 0
        self.formation_name: str = ""
        self.formation: Dict[str, Union[int, bool, List[List[str]]]] = {}
        self.is_chain_reply: bool = tarot_config.chain_reply
        self.devined: List[str] = []
        self.is_cut: bool = False
        self.represent: List[str] = []
        
    async def divine(self) -> Tuple[MessageSegment, int]:
        '''
            Get one formation of all formations
        '''
        self.formation_name = random.choice(list(self._formations))
        formation = self._formations.get(self.formation_name)
        self.cards_num = formation.get("cards_num")
        self.devined = random.sample(list(self._cards), self.cards_num)
        self.is_cut = formation.get("is_cut")
        self.represent = random.choice(formation.get("represent"))
        
        return MessageSegment.text(f"启用{self.formation_name}，正在洗牌中"), self.cards_num

    async def reveal(self, cards_index: int) -> MessageSegment:
        '''
            cards_index: 0 to cards_num-1
        '''
        if self.is_cut and cards_index == self.cards_num:
            msg_header = MessageSegment.text(f"切牌，代表{self.represent[cards_index]}\n")
        else:
            msg_header = MessageSegment.text(f"第{cards_index+1}张牌，代表{self.represent[cards_index]}\n")
        
        card = self._cards.get(self.devined[cards_index])
        name_cn = card.get("name_cn")
        img_path = Path(self.tarot_json / card.get("type") / card.get("pic"))
        img = Image.open(img_path)
        
        if random.random() < 0.5:
            # 正位
            meaning = card.get("meaning").get("up")
            msg = MessageSegment.text(f"{name_cn}正位，代表{meaning}\n")  
        else:
            meaning = card.get("meaning").get("down")
            msg = MessageSegment.text(f"{name_cn}逆位，代表{meaning}\n")
            img = img.rotate(180)
        
        buf = BytesIO()
        img.save(buf, format='png')
        
        return msg_header + msg + MessageSegment.image(buf)
    
    def switch_chain_reply(self, new_state: bool) -> None:
        '''
            开启/关闭群聊转发模式
        '''
        self.is_chain_reply = new_state

tarot_manager = Tarot()