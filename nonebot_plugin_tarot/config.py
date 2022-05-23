from pydantic import BaseModel, Extra
from pathlib import Path 
from typing import Set
import httpx
from aiocache import cached
import nonebot
from nonebot import logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class PluginConfig(BaseModel, extra=Extra.ignore):
    tarot_path: Path = Path(__file__).parent / "resource"
    chain_reply: bool = False
    nickname: Set[str] = {"Bot"}

driver = nonebot.get_driver()
tarot_config: PluginConfig = PluginConfig.parse_obj(driver.config.dict())

class DownloadError(Exception):
    pass

async def download_url(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                response = await client.get(url)
                if response.status_code != 200:
                    continue
                return response
            except Exception as e:
                logger.warning(f"Error occured when downloading tarot.json, {i+1}/3: {e}")
    
    raise DownloadError

@driver.on_startup
async def tarot_version_check() -> None:
    '''
        Get the latest version of tarot.json
    '''
    if not tarot_config.tarot_path.exists():
        tarot_config.tarot_path.parent.mkdir(parents=True, exist_ok=True)
        
    url = "https://cdn.jsdelivr.net/gh/MinatoAquaCrews/nonebot_plugin_tarot@beta/resource/tarot.json"
    response = await download_url(url)
    docs = response.json()
    version = docs.get("version")

    with tarot_config.tarot_path.open("w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=4)
        logger.info(f"Get the latest tarot docs in repo, version: {version}")

@cached(ttl=180)
async def get_tarot(_type: str, _name_cn: str) -> bytes:
    '''
        Download tarot image if TAROT_LOCAL is disable
    '''
    if not tarot_config.tarot_path.exists():
        tarot_config.tarot_path.parent.mkdir(parents=True, exist_ok=True)
        
    url = f"https://cdn.jsdelivr.net/gh/MinatoAquaCrews/nonebot_plugin_tarot@beta/resource/{_type}/{_name_cn}"
    data = await download_url(url)
    return data.content()