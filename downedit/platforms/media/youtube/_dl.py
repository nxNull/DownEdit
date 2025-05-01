import httpx
from typing import Optional, Dict


from downedit.service import httpx_capture_async, retry_async
from downedit.platforms import Domain
from downedit.platforms.media.youtube.client import YoutubeClient
from downedit.download import Downloader
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


class YoutubeDL:
    def __init__(self, *args, **kwargs) -> None:
        self.user_agent = UserAgent(
            platform_type="desktop",
            device_type="windows",
            browser_type="chrome"
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            Sec-Ch-Ca,
            Sec-Ch-Ua-Platform,
            Sec-Ch-Ua-Mobile,
        """)
        self.default_client = Client(headers=self.headers.get())
        self.client: Client = kwargs.get("client", self.default_client)
        self.yt_client = YoutubeClient()
        self.observer = Observer()

    @httpx_capture_async
    @retry_async(
        num_retries=3,
        delay=1,
        exceptions=(
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
            httpx.ProxyError,
            httpx.UnsupportedProtocol,
            httpx.StreamError,
        ),
    )
    async def _get_player_response(self, video_id: str) -> Optional[Dict]:
        """
        Gets the player response for the video.

        Args:
            video_id (str): The video identifier.

        Returns:
            dict: A dictionary containing the player response.
        """
        client_details = self.yt_client.get_client_details()
        payload = await self.yt_client.create_payload(video_id)
        headers = await self.yt_client.create_headers(client_details)
        response = await Client().aclient.post(
            url=Domain.YOUTUBE.YT_PLAYER,
            json=payload,
            headers=headers,
        )

        response.raise_for_status()
        return response.json()

    async def _get_video_response(self, video_id: str) -> tuple[Optional[str], Optional[str]]:
        """
        Get the video response for the given video ID.

        Returns:
            A tuple containing:
                - The URL of the highest quality video (str or None).
                - The URL of the M4A audio stream (str or None).
        """
        async with self.client.semaphore:
            response = await self.client.aclient.post(
                url="https://www.clipto.com/api/youtube",
                json={"url": F"https://www.youtube.com/watch?v={video_id}"},
                timeout=10,
                follow_redirects=True,
            )
            response.raise_for_status()

        data = response.json()
        medias = data.get("medias")
        if not medias: return None, None

        best_video = max(
            (m for m in medias if m["type"] == "video" and m["ext"] == "mp4"),
            key=lambda m: m.get("height", -1),
            default=None
        )
        best_audio = max(
            (m for m in medias if m["type"] == "audio" and m["ext"] == "m4a"),
            key=lambda m: m.get("bitrate", -1),
            default=None
        )

        return best_video and best_video.get("url"), best_audio and best_audio.get("url")

    async def download_video(
        self,
        video_url: str,
        video_name: str = "starting...",
        output_folder: str = "./"
    ):
        """
        Downloads the video from the provided URL.

        Args:
            video_url (str): The URL of the video to download.
            video_name (str, optional): Defaults to "starting...".
            output_folder (str, optional): The folder to save the downloaded video. Defaults to "./".
        """
        player_response = await self._get_player_response(video_url)
        if player_response is None:
            log.error("No player response found.")
            return

        video_stream = player_response.get("streamingData", {}).get("adaptiveFormats", [])
        if not video_stream:
            log.error("No video stream found.")
            return

        client = Client()
        client.headers["User-Agent"] = self.yt_client.get_client_details()["userAgent"]

        async with Downloader(client) as downloader:
            await downloader.add_file(
                file_url=video_stream[0].get("url", ""),
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
        output_folder: str
    ):
        """
        Downloads multiple videos from the provided URL list.

        Args:
            video_list (list[dict[str, str]]): The list of video URLs to download.
            output_folder (str): The folder to save the downloaded videos.
        """
        self.observer.register_termination_handlers()
        client = Client(headers=self.headers.get())

        async with Downloader(client) as downloader:
            for video in video_list:
                if self.observer.is_termination_signaled():
                    break

                video_url = await self._get_video_response(
                    video.get("video_id")
                )
                if not video_url[0]: continue

                file_paths = []
                for index, url in enumerate(video_url):
                    file_extension = ".mp4" if index == 0 else ".mp3"
                    file_name = f"{video.get('video_title')} part_{index}{file_extension}"
                    file_output = ResourceUtil.normalize_filename(
                        folder_location=output_folder,
                        file_name=str(video.get("video_title")) + f" part_{index}",
                        file_extension=file_extension
                    )
                    file_paths.append(file_output)

                    await downloader.add_file(
                        file_url=url,
                        file_media=(
                            file_output,
                            file_name
                        )
                    )
                await downloader.execute()

            await downloader.close()
