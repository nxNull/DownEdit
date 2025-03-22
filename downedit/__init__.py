r"""
DownEdit

This module provides tools for downloading, editing, and generating videos, images, and sounds in bulk using AI.
It includes functionalities for handling various media types, interfacing with popular platforms, and AI-driven media processing.

Author: Sokunheng
Version: 1.0.1
Repository: https://github.com/sokunheng/DownEdit
"""

from downedit.__config__ import (
    CHUNK_SIZE,
    DE_VERSION,
    Config,
    EditFolder,
    MediaFolder,
    Extensions,
    AIContext
)

from downedit.edit import (
    VideoProcess as Video,
    SoundProcess as Sound,
    ImageProcess as Image,
    AIImgEditProcess as AIEditImg,
)

from downedit.platforms import (
    Domain,
    Douyin,
    KuaiShou,
    Tiktok,
    Youtube
)

from downedit.service import (
    retry_sync,
    httpx_capture_sync,
    retry_async,
    httpx_capture_async,
    Client,
    ClientHints,
    Headers,
    Proxy,
    UserAgent,
    Fingerprint
)

from downedit.edit.ai.cloud import AIImgGenProcess as AIGenImgCloud
from downedit.download import Downloader

__author__          = "sokunheng"
__version__         = "1.0.1"
__description_en__  = "Download, Edit, and Generate Videos, Images and Sounds, in bulk using AI"
__reponame__        = "DownEdit"
__repourl__         = "https://github.com/sokunheng/DownEdit"

__all__ = [
    "CHUNK_SIZE",
    "DE_VERSION",
    "Config",
    "EditFolder",
    "MediaFolder",
    "Extensions",
    "AIContext",

    "Video",
    "Sound",
    "Image",
    "AIEditImg",
    "AIGenImgCloud",

    "retry_sync",
    "httpx_capture_sync",
    "retry_async",
    "httpx_capture_async",
    "Client",
    "ClientHints",
    "Headers",
    "Proxy",
    "UserAgent",
    "Fingerprint",
    "Downloader",

    "Domain",
    "Douyin",
    "KuaiShou",
    "Tiktok",
    "Youtube",

    "__author__",
    "__version__",
    "__description_en__",
    "__reponame__",
    "__repourl__"
]