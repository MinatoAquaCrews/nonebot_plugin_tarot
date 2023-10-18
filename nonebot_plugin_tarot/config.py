from pathlib import Path
from typing import List, Set, Optional, Union

import httpx
import nonebot
import nonebot_plugin_localstore as store
from aiocache import cached
from nonebot import logger
from pydantic import BaseModel, Extra

try:
    import ujson as json  # type: ignore
except ModuleNotFoundError:
    import json


class PluginConfig(BaseModel, extra=Extra.ignore):
    tarot_path: Path = store.get_data_dir("nonebot_plugin_tarot")
    """Directory of tarot image resources. \
        Required if the images are deployed locally."""

    chain_reply: bool = True
    """Enable the chain reply for avoiding \
        screen spamming in group chat."""

    nickname: Set[str] = {"Bot"}
    """Bot's nickname."""

    tarot_builtin_theme_enabled: bool = True

    tarot_extra_themes: Union[Set[str], List[str]] = []
    """Extra tarot themes. Both `set` and `list` types are supported."""


driver = nonebot.get_driver()
tarot_config: PluginConfig = PluginConfig.parse_obj(
    driver.config.dict(exclude_unset=True)
)


class DownloadError(Exception):
    pass


class ResourceError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


async def download_url(name: str) -> Optional[httpx.Response]:
    url: str = (
        "https://raw.fgit.cf/MinatoAquaCrews/nonebot_plugin_tarot/master/nonebot_plugin_tarot/"
        + name
    )

    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                response = await client.get(url)
                if response.status_code != 200:
                    continue

                return response

            except Exception:
                logger.warning(f"Error occurred when downloading {url}, retry: {i+1}/3")

    logger.warning("Abort downloading")


@driver.on_startup
async def tarot_config_check() -> None:
    """Check the theme configuration & text reource on startup."""
    if (
        not tarot_config.tarot_builtin_theme_enabled
        and len(tarot_config.tarot_extra_themes) == 0
    ):
        raise ResourceError(
            "No available themes! Please make sure at least 1 theme is enabled.\n"
            "See https://github.com/MinatoAquaCrews/nonebot_plugin_tarot/blob/master/README.md for details."
        )

    # If a custom directory is provided by user, check if it exists.
    p = tarot_config.tarot_path
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
    elif not p.is_dir():
        raise RuntimeError(f"{p} is not a directory")

    # Check whether tarot.json. exists
    tarot_json_path = Path(__file__).parent / "tarot.json"

    if not tarot_json_path.exists():
        logger.warning("Missing text resource tarot.json! Trying to download...")
        response = await download_url("tarot.json")

        if not response:
            raise DownloadError

        with tarot_json_path.open("w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
            logger.info(f"Downloaded completed. Saved to {tarot_json_path}.")


@cached(ttl=180)
async def get_tarot(theme: str, type: str, name: str) -> Optional[bytes]:
    """Download the image and cache it for a while. \
        If failed, return None.
    """
    logger.info(f"Downloading image {theme}/{type}/{name} from repo...")

    resource = f"resource/{theme}/{type}/{name}"
    response = await download_url(resource)

    if not response:
        logger.warning(f"Download image {theme}/{type}/{name} failed!")
        return None

    return response.content
