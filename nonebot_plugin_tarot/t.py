from nonebot.adapters.onebot.v11 import MessageSegment
import random
from pathlib import Path 
from typing import List, Dict, Union, Tuple
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class Tarot:
    def __init__(self):
        self._init_json_ok: bool = False
        self._formations: Dict[str, Dict[str, Union[int, bool, List[List[str]]]]] = {}
        self._cards: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = {}
        self.cards_num: int = 0
        # self.is_chain_reply: bool = tarot_config.chain_reply
        self.devined: List[str] = []
        self.is_cut: bool = False
        self.represent: List[str] = []
    
    def init_json(self):
        tarot_json: Path = Path(__file__).parent / "resource" / "tarot.json"
        with open(tarot_json, 'r', encoding='utf-8') as f:
            content = json.load(f)
            self._formations = content.get("formation")
            self._cards = content.get("cards")
        
        self._init_json_ok = True
        
    async def divine(self) -> Tuple[MessageSegment, int]:
        '''
            Get one formation of all formations
        '''
        if not self._init_json_ok:
            self.init_json()
            
        formation_name = random.choice(list(self._formations))
        formation = self._formations.get(formation_name)
        self.cards_num = formation.get("cards_num")
        self.devined = random.sample(list(self._cards), self.cards_num)
        self.is_cut = formation.get("is_cut")
        self.represent = random.choice(formation.get("represent"))
        
        return MessageSegment.text(f"启用{formation_name}，正在洗牌中"), self.cards_num

    # async def reveal(self, index: int) -> MessageSegment:
    #     '''
    #         index: 0 to cards_num-1
    #     '''
    #     if self.is_cut and index == self.cards_num - 1:
    #         msg_header = MessageSegment.text(f"切牌「{self.represent[index]}」\n")
    #     else:
    #         msg_header = MessageSegment.text(f"第{index+1}张牌「{self.represent[index]}」\n")
        
    #     msg_body: MessageSegment = await self.multi_divine(index)
        
    #     return msg_header + msg_body
        
    def multi_divine(self, index: int) -> None:
        '''
            Multi divines, arrcording to index get the meaning and image(up or down)
        '''
        card: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = self._cards.get(self.devined[index])
        name_cn: str = card.get("name_cn")
        print(card.get("type"), card.get("pic"))
    
    def single_divine(self) -> MessageSegment:
        '''
            Single divine, get a tarot
        '''
        if not self._init_json_ok:
            self.init_json()
              
        self.devined = [random.choice(list(self._cards))]
        print(self.devined)
        msg = MessageSegment.text("回应是")
        self.multi_divine(0)
        
        return msg

if __name__ == "__main__":
    tarot_manager = Tarot()
    tarot_manager.single_divine()
    print(type(tarot_manager.devined))