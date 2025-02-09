import asyncio
import secrets
import traceback
import re

from downedit.platforms.media.kuaishou._dl import KuaishouDL
from downedit.platforms.media.kuaishou.crawler import KuaishouCrawler
from downedit.platforms.media.kuaishou.extractor import (
    extract_user_id,
    extract_url_segment
)
from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)

class KuaiShou:
    def __init__(self, user, **kwargs):
        self.user = user
        self.cookies = kwargs.get("cookies", "")
        self.observer = Observer()
        self._output_folder = self._get_output_folder()
        self.kuaishou_crawler = KuaishouCrawler(cookies=self.cookies)
        self.kuaishou_dl = KuaishouDL(
            output_folder=self._output_folder
        )

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for KUAISHOU video.
        """
        return ResourceUtil.create_folder(
            folder_type="KUAISHOU"
        )

    async def download(self, video_url: str, video_name: str = "starting..."):
        """
        Downloads the video from the provided URL.
        """
        try:
            await self.kuaishou_dl.download_video(
                video_url = video_url,
                video_name = video_name
            )
        except Exception as e:
            log.error(traceback.format_exc())
            log.pause()

    async def download_all_videos_async(self):
        """
        Asynchronously downloads all videos from the user.
        """
        user_id = extract_user_id(self.user)
        # async for video in self.kuaishou_crawler.fetch_user__videos(user_id):
        #     if self.observer.is_termination_signaled():
        #             break

        #     await self.download(
        #         video_url=video["playUrl"],
        #         video_name=self.extract_live_url_segment(video["playUrl"])
        #     )
        async for video in self.kuaishou_crawler.fetch_user_feed_videos(user_id):
            if self.observer.is_termination_signaled():
                    break

            await self.download(
                video_url=video,
                video_name=extract_url_segment(video)
            )

    def download_all_videos(self):
        """
        Download all videos from the user
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(
                self.download_all_videos_async()
            )
        except Exception as e:
            log.error(traceback.format_exc())

