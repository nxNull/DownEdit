import asyncio
import traceback

from downedit.platforms.media.youtube._dl import YoutubeDL
from downedit.platforms.media.youtube.crawler import YouTubeCrawler
from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)

class Youtube:
    def __init__(self, **kwargs):
        self.observer = Observer()
        self._output_folder = self._get_output_folder()
        self.youtube_crawler = YouTubeCrawler()
        self.youtube_dl = YoutubeDL(
            output_folder=self._output_folder
        )

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for youtube video.
        """
        return ResourceUtil.create_folder(
            folder_type="YOUTUBE"
        )

    async def download(self, video_url: str, video_name: str = "starting..."):
        """
        Downloads the video from the provided URL.
        """
        try:
            await self.youtube_dl.download_video(
                video_url = video_url,
                video_name = video_name,
                output_folder= self._output_folder
            )
        except Exception as e:
            log.error(traceback.format_exc())
            log.pause()

    async def download_all_videos_async(
        self,
        channel_url: str = None,
        video_type: str = None
    ):
        """
        Download all videos from the channel asynchronously
        """
        async for video in self.youtube_crawler.aget_channel(
            channel_url=channel_url,
            content_type=video_type
        ):
            if self.observer.is_termination_signaled():
                    break

            await self.download(
                video_url=video["videoId"],
                # video_name = video["title"]["accessibility"]["accessibilityData"]["label"]
                video_name=video["title"]["runs"][0]["text"]
            )

    def download_all_videos(
        self,
        channel_url: str = None,
        video_type: str = None
    ):
        """
        Download all videos from the channel
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(
                self.download_all_videos_async(
                    channel_url=channel_url,
                    video_type=video_type
                )
            )
        except Exception as e:
            log.error(traceback.format_exc())
