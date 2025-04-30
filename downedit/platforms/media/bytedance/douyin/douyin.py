import asyncio
from datetime import datetime
import traceback

from downedit.platforms.media.bytedance.douyin._dl import DouyinDL
from downedit.platforms.media.bytedance.douyin.crawler import DouyinCrawler
from downedit.platforms.media.bytedance.douyin.extractor import extract_username
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    console,
    column,
    ResourceUtil,
    Observer,
    log
)


class Douyin:

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
            sec-ch-ua-platform,
            sec-ch-ua-mobile,
        """)
        self.default_client = Client(headers=self.headers.get())
        self.cookies = kwargs.get("cookies", "")
        self.douyin_crawler = DouyinCrawler(
            client=self.default_client,
            cookies=self.cookies
        )
        self.douyin_dl = DouyinDL(
            client=self.default_client
        )

        self.observer = Observer()
        self.task_progress = console().progress_bar(
            column_config=column().wait()
        )
        self._output_folder = self._get_output_folder()
        self.video_list: list[list[dict[str, str]]] = []

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for downloading videos.
        """
        return ResourceUtil.create_folder(
            folder_type="DOUYIN"
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

                await self.douyin_dl.download_multiple_videos(
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
        video_bitrates = item.get("bit_rate", [])

        if not video_bitrates:
            return None, "no video"

        play_addr = video_bitrates.get("play_addr", {})
        url_list = play_addr.get("url_list", [])

        video_desc = item.get("desc").encode('latin1').decode('utf-8')
        datetime_object = datetime.fromtimestamp(item.get("create_time", 0))
        upload_date = datetime_object.strftime("%Y-%m-%d")
        video_title = f"{upload_date} - {video_desc}"

        return url_list[0], video_title

    def _process_item_list(self, item_list):
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

    async def download_all_videos_async(self, user_url: str = "") -> None:
        """
        Asynchronously fetches and downloads all videos from a user's TikTok feed.
        """
        user_folder_name = ResourceUtil.folder(
            folder_root=self._output_folder,
            directory_name=extract_username(user_url)
        )

        task_id = await self.task_progress.add_task(
            description="Getting videos",
            file_name=extract_username(user_url),
            total_units=None,
            start=True,
            current_state="idle",
        )

        with self.task_progress:
            await self.task_progress.update_task(
                task_id,
                new_state="starting",
                force_refresh=True
            )

            max_cursor, count, has_more = 0, 18, True

            while has_more:
                user_feed = await self.douyin_crawler.fetch_user_post(
                    sec_uid=extract_username(user_url),
                    max_cursor=max_cursor,
                    count=count,
                )

                if not user_feed: break

                item_list = user_feed.get("aweme_list") or []
                if not item_list:
                    break

                has_more = user_feed.get("has_more", 0) == 1
                max_cursor = user_feed.get("max_cursor", max_cursor)

                self._process_item_list(item_list)

            await self.task_progress.update_task(
                task_id=task_id,
                new_description="Done",
                new_state="success"
            )

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
                self.download_all_videos_async(user_url=user)
            )
        except Exception as e:
            log.error(traceback.format_exc())
