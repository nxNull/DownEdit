from datetime import datetime

from downedit.service import httpx_capture_async, retry_async
from downedit.download import Downloader
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    ResourceUtil,
    log
)


class DouyinDL:
    def __init__(self, *args, **kwargs) -> None:
        self.user_agent = UserAgent(
            platform_type="desktop",
            device_type="windows",
            browser_type="chrome"
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            sec-ch-ua,
            sec-ch-ua-platform,
            sec-ch-ua-mobile,
        """)
        self.default_client = Client(headers=self.headers.get())
        self.client: Client = kwargs.get("client", self.default_client)

    async def download_video(
        self,
        video_url: str,
        video_name: str = "starting...",
        output_folder: str = "./"
    ):
        """
        Downloads the video from the provided URL.
        """
        client = Client()
        client.headers = self.client.headers

        async with Downloader(client) as downloader:
            await downloader.add_file(
                file_url=video_url,
                file_media=(
                    ResourceUtil.normalize_filename(
                        folder_location=output_folder,
                        file_name=video_name,
                        file_extension=".mp4"
                    ),
                    video_name
                )
            )
            await downloader.execute()
            await downloader.close()

    async def download_multiple_videos(
        self,
        video_list: list[dict[str, str]],
        output_folder: str = "./"
    ):
        """
        Downloads multiple videos from the provided URLs.
        """
        client = Client()
        client.headers = self.client.headers

        async with Downloader(client) as downloader:
            for video in video_list:
                video_url = video.get("video_url", None)
                video_name = video.get("video_title", datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

                if not video_url:
                    continue

                await downloader.add_file(
                    file_url=video_url,
                    file_media=(
                        ResourceUtil.normalize_filename(
                            folder_location=output_folder,
                            file_name=video_name,
                            file_extension=".mp4"
                        ),
                        video_name
                    )
                )

            await downloader.execute()
            await downloader.close()
