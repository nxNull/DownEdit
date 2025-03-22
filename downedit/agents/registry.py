from downedit.edit.ai.cloud.image import AIImgGenProcess
from downedit.platforms import (
    Youtube,
    KuaiShou
)
from downedit.edit import (
    VideoProcess,
    SoundProcess,
    ImageProcess
)

__all__ = ["get_tool"]


TOOLS = {}
TOOLS["edit_video"] = VideoProcess
TOOLS["edit_image"] = ImageProcess
TOOLS["edit_sound"] = SoundProcess
TOOLS["generate_ai_image"] = AIImgGenProcess
# TOOLS["generate_ai_sound"] = AISoundGenProcess
# TOOLS["generate_ai_video"] = AIVidGenProcess
# TOOLS["tiktok_downloader"] = Tiktok
# TOOLS["douyin_downloader"] = Douyin
TOOLS["youtube_downloader"] = Youtube
# TOOLS["kuaishou_downloader"] = KuaiShou


def get_tool(tool_name: str):
    """
    Retrieves the tool class from the registry.

    Args:
        tool_name (str): The name of the tool to retrieve.
    """
    return TOOLS.get(tool_name)