import asyncio
import traceback

from downedit.platforms.media.youtube._dl import YoutubeDL
from downedit.platforms.media.youtube.crawler import YouTubeCrawler
from downedit.platforms.media.youtube.extractor import extract_channel_handle
from downedit.utils import (
    console,
    column,
    ResourceUtil,
    Observer,
    log
)


class Youtube:
    def __init__(self, **kwargs):
        self.youtube_crawler = YouTubeCrawler()
        self.youtube_dl = YoutubeDL()

        self.observer = Observer()
        self.task_progress = console().progress_bar(
            column_config=column().edit()
        )
        self._output_folder = self._get_output_folder()
        self.video_list: list[dict[str, str]] = []

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for youtube video.
        """
        return ResourceUtil.create_folder(
            folder_type="YOUTUBE"
        )

    async def download_multiple(
        self,
        video_list: list[dict[str, str]],
        output_folder: str
    ):
        """
        Downloads multiple videos from the provided URL list.
        """
        try:
            await self.youtube_dl.download_multiple_videos(
                video_list=video_list,
                output_folder=output_folder
            )
        except Exception as e:
            log.error(traceback.format_exc())
            log.pause()

    def __extract_video_info(self, item):
        """
        Extract the video from a feed item.

        Returns:
            Tuple[str or None, str]: The video ID (if available) and video title.
        """
        video_id = item.get('videoId', "")

        video_title = item.get('title', {}).get("runs", [])[0].get("text", "")
        if not video_title:
            video_title = f"video_{video_id}"

        video_title = f"{video_id} - {video_title}"

        return video_id, video_title

    def _process_item_list(self, data):
        """
        Process the item list and extract video URLs and titles.
        """
        video_id, video_title = self.__extract_video_info(data)

        self.video_list.append({
            "video_id": video_id,
            "video_title": video_title
        })

    async def download_all_videos_async(
        self,
        channel_url: str = None,
        video_type: str = None
    ):
        """
        Download all videos from the channel asynchronously
        """
        channel_folder_name = ResourceUtil.folder(
            folder_root=self._output_folder,
            directory_name=extract_channel_handle(channel_url)
        )

        task_id = await self.task_progress.add_task(
            description="Getting videos",
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

            async for video in self.youtube_crawler.aget_channel(
                channel_url=channel_url,
                content_type=video_type
            ):
                if self.observer.is_termination_signaled():
                        break

                self._process_item_list(video)

            await self.task_progress.update_task(
                task_id=task_id,
                new_completed=100,
                new_description="Done",
                new_state="success"
            )

        await self.download_multiple(
            video_list=self.video_list,
            output_folder=str(channel_folder_name)
        )
        self.video_list.clear()

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
