import asyncio
from datetime import datetime
import traceback

from downedit.platforms.media.kuaishou._dl import KuaishouDL
from downedit.platforms.media.kuaishou.crawler import KuaishouCrawler
from downedit.platforms.media.kuaishou.extractor import (
    extract_user_id,
    extract_url_segment
)
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

class KuaiShou:
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
        self.kuaishou_crawler = KuaishouCrawler(
            client=self.default_client,
            cookies=self.cookies
        )
        self.kuaishou_dl = KuaishouDL(
            client=self.default_client
        )

        self.observer = Observer()
        self.task_progress = console().progress_bar(
            column_config=column().edit()
        )
        self._output_folder = self._get_output_folder()
        self.video_list: list[list[dict[str, str]]] = []

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for KUAISHOU video.
        """
        return ResourceUtil.create_folder(
            folder_type="KUAISHOU"
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

                await self.kuaishou_dl.download_multiple_videos(
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
        photo = item.get("photo", {})
        manifest = photo.get("manifest", {})
        adaptationSet = manifest.get("adaptationSet", [])

        if not adaptationSet:
            return None, "no video"

        url_list = adaptationSet[0].get("representation", [])[0]
        video_url = url_list.get("url", "")

        if not video_url:
            return None, "no video"

        video_desc = photo.get("originCaption")
        timestamp_ms = photo.get("timestamp", 0)
        timestamp_s = timestamp_ms / 1000 if timestamp_ms else 0
        datetime_object = datetime.fromtimestamp(timestamp_s)
        upload_date = datetime_object.strftime("%Y-%m-%d")
        video_title = f"{upload_date} - {video_desc}"

        return video_url, video_title

    def _process_item_list(self, data):
        """
        Process and download videos from a batch of feed items.
        """
        current_video_batch = []
        feeds = data.get("feeds", [])

        for item in feeds:
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

    async def download_all_videos_async(self, user_id: str = ""):
        """
        Asynchronously downloads all videos from the user.
        """
        user_folder_name = ResourceUtil.folder(
            folder_root=self._output_folder,
            directory_name=extract_user_id(user_id)
        )
        task_id = await self.task_progress.add_task(
            description="Getting videos",
            file_name=extract_user_id(user_id),
            total_units=100,
            units_done=0,
            start=True,
            current_state="idle",
        )

        with self.task_progress:
            await self.task_progress.update_task(
                task_id,
                new_state="starting",
                force_refresh=True
            )

            pcursor, count, has_more = "", 18, True

            while has_more:
                user_feed = await self.kuaishou_crawler.fetch_user_feed_videos(
                    principalId=extract_user_id(user_id),
                    pcursor=pcursor,
                    count=count,
                )

                if not user_feed: break

                visionProfilePhotoList = user_feed.get("data", {}).get("visionProfilePhotoList", {})

                pcursor = visionProfilePhotoList.get("pcursor", "")
                has_more = visionProfilePhotoList.get("result", 0) == 1 or pcursor == "no_more"

                self._process_item_list(visionProfilePhotoList)

            await self.task_progress.update_task(
                task_id=task_id,
                new_completed=100,
                new_description="Finished",
                new_state="success"
            )

        await self.download_multiple(
            video_list=self.video_list,
            output_folder=str(user_folder_name)
        )
        self.video_list.clear()

    def download_all_videos(self, user: str = ""):
        """
        Download all videos from the user
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(
                self.download_all_videos_async(user)
            )
        except Exception as e:
            log.error(traceback.format_exc())

