import asyncio
import datetime
import traceback

from downedit.platforms.media.bytedance.tiktok._dl import TikTokDL
from downedit.platforms.media.bytedance.tiktok.crawler import TiktokCrawler
from downedit.platforms.media.bytedance.tiktok.extractor import extract_username
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)


class Tiktok:

    def __init__(self, **kwargs):
        self.user_agent = UserAgent(
            platform_type='desktop',
            device_type='windows',
            browser_type='chrome'
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            sec-ch-ua,
            sec-ch-ua-full-version-list,
            sec-ch-ua-platform,
            sec-ch-ua-platform-version,
            sec-ch-ua-mobile,
            sec-ch-ua-bitness,
            sec-ch-ua-arch,
            sec-ch-ua-model,
            sec-ch-ua-wow64
        """)
        self.default_client = Client(headers=self.headers.get())
        self.cookies = kwargs.get("cookies", "")
        self.tiktok_crawler = TiktokCrawler(
            client=self.default_client,
            cookies=self.cookies
        )
        self.tiktok_dl = TikTokDL(
            client=self.default_client
        )

        self.observer = Observer()
        self._output_folder = self._get_output_folder()
        self.video_list: list[list[dict[str, str]]] = []

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for downloading videos.
        """
        return ResourceUtil.create_folder(
            folder_type="TIKTOK"
        )

    async def download_multiple(
        self,
        video_list: list[dict[str, str]],
        output_folder: str
    ):
        """
        Downloads the video from the provided URL list.
        """
        try:
            for videos in video_list:
                if self.observer.is_termination_signaled():
                    break

                await self.tiktok_dl.download_multiple_videos(
                    video_list=videos,
                    output_folder=output_folder
                )
        except Exception as e:
            log.error(traceback.format_exc())
            log.pause()

    def __extract_video_info(self, item):
        """
        Extract the video from a feed item.

        Returns:
            Tuple[str or None, str]: The video URL (if available) and video title.
        """
        video_info = item.get("video", {})
        bitrate_info = video_info.get("bitrateInfo", [])

        if not bitrate_info:
            return None, "no video"

        # Select the highest quality video by default
        # This selects the first bitrate info entry (usually the highest quality).
        play_addr = bitrate_info[0].get("PlayAddr", {})
        url_list = play_addr.get("UrlList", [])

        video_url = url_list[0] if url_list else None
        video_desc = item.get("desc", "no title")

        # t
        video_url = item.get("id", "")
        video_url = f'https://www.tikwm.com/video/media/hdplay/{video_url}.mp4'

        datetime_object = datetime.datetime.fromtimestamp(item.get("createTime", 0))
        upload_date = datetime_object.strftime("%Y-%m-%d")
        video_title = f"{upload_date} - {video_desc}"

        return video_url, video_title

    async def _process_item_list(self, item_list):
        """
        Process and download videos from a batch of feed items.
        """
        current_video_batch = []
        for item in item_list:
            video_url, video_title = self.__extract_video_info(item)

            current_video_batch.append({
                "video_url": video_url,
                "video_title": video_title
            })

            if len(current_video_batch) >= 5:
                self.video_list.append(current_video_batch)
                current_video_batch = []

        if current_video_batch:
            self.video_list.append(current_video_batch)

    async def download_all_videos_async(self, username: str = "") -> None:
        """
        Asynchronously fetches and downloads all videos from a user's TikTok feed.
        """
        user_folder_name = ResourceUtil.folder(
            folder_root=self._output_folder,
            directory_name=extract_username(username)
        )
        cursor, count, has_more = 0, 35, True

        while has_more:
            user_feed = await self.tiktok_crawler.fetch_user_post(
                user_url=username,
                cursor=cursor,
                count=count,
            )

            item_list = user_feed.get("itemList") or []
            if not item_list:
                break

            has_more = user_feed.get("hasMore", False)
            cursor = user_feed.get("cursor", cursor)

            await self._process_item_list(item_list)

        await self.download_multiple(
            video_list=self.video_list,
            output_folder=str(user_folder_name)
        )
        self.video_list.clear()

    def download_all_videos(self, user: str = ""):
        """
        Download all videos from the channel
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(
                self.download_all_videos_async(username=user)
            )
        except Exception as e:
            log.error(traceback.format_exc())
