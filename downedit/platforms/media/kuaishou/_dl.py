from downedit.service import httpx_capture_async, retry_async
from downedit.download import Downloader
from downedit.service import (
    Client
)
from downedit.utils import (
    ResourceUtil,
    log
)

class KuaishouDL:
    def __init__(self, output_folder: str):
        self.output_folder = output_folder

    async def download_video(self, video_url: str, video_name: str = "starting..."):
        """
        Downloads the video from the provided URL.
        """
        client = Client()
        async with Downloader(client) as downloader:
            await downloader.add_file(
                file_url=video_url,
                file_media=(
                    ResourceUtil.normalize_filename(
                        folder_location=self.output_folder,
                        file_name=video_name,
                        file_extension=".mp4"
                    ),
                    video_name
                )
            )
            await downloader.execute()
            await downloader.close()