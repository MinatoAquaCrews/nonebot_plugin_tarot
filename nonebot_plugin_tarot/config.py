from pydantic import BaseModel, Extra
from pathlib import Path 
from typing import Set
import httpx
from aiocache import cached
import aiofiles
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

class ResourceError(Exception):
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
        tarot_config.tarot_path.mkdir(parents=True, exist_ok=True)
        
    url = "https://raw.fastgit.org/MinatoAquaCrews/nonebot_plugin_tarot/beta/nonebot_plugin_tarot/resource/tarot.json"
    response = await download_url(url)
    docs = response.json()
    version = docs.get("version")
    
    json_path = tarot_config.tarot_path / "tarot.json"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=4)
        logger.info(f"Get the latest tarot docs in repo, version: {version}")

@cached(ttl=180)
async def get_tarot(_type: str, _name_cn: str) -> bytes:
    '''
        Download tarot image
    '''
    img_path = tarot_config.tarot_path / _type / _name_cn

    if not img_path.parent.exists():
        img_path.parent.mkdir(parents=True, exist_ok=True)
        
    url = f"https://raw.fastgit.org/MinatoAquaCrews/nonebot_plugin_tarot/beta/nonebot_plugin_tarot/resource/{_type}/{_name_cn}"
    data = await download_url(url)
    if data.content():
        async with aiofiles.open(img_path, "w") as f:
            await f.write(data.content())
            
    if not img_path.exists():
        raise ResourceError
    
    async with aiofiles.open(img_path, "r") as f:
        return await f.read()