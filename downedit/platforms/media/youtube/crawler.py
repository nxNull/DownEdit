import asyncio
import httpx
import json

from typing import AsyncGenerator, Dict, Generator, Optional, Tuple
from typing_extensions import Literal

from downedit.platforms.domain import Domain
from downedit.utils import (
    log
)
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)

TYPE_PROPERTY_MAP = {
    "videos": "videoRenderer",
    "streams": "videoRenderer",
    "shorts": "reelWatchEndpoint"
}
SORT_BY_MAP = {
    "newest": 0,
    "popular": 1,
    "oldest": 2,
}
SORT_BY_VALUES = {
    "relevance": "A",
    "upload_date": "I",
    "view_count": "M",
    "rating": "E"
}
RESULTS_TYPE_VALUES = {
    "video": ["B", "videoRenderer"],
    "channel": ["C", "channelRenderer"],
    "playlist": ["D", "playlistRenderer"],
    "movie": ["E", "videoRenderer"]
}

class YouTubeCrawler:
    """
    Asynchronous YouTube Crawler that fetches video data from YouTube.

    This class provides methods to retrieve videos from channels, playlists, search queries, and more.
    """

    def __init__(self, client: Client = None):
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
        self.client = client or self.default_client

    async def _aget_initial_data(
        self,
        url: str,
        params: dict = None
    ) -> Tuple[str, dict]:
        """
        Retrieves initial HTML and client context from a YouTube page.

        Parameters:
            url (str): The URL of the YouTube page.
            params (dict, optional): Optional parameters for the GET request. Defaults to {"ucbcb": 1}.

        Returns:
            Tuple[str, dict]: The HTML response as a string and the client context as a dictionary.
        """
        self.client.headers["Cookie"] = "CONSENT=YES+cb"
        self.client.headers["Host"] = "www.youtube.com"
        self.client.headers["Referer"] = Domain.YOUTUBE.DOMAIN

        response = await self.client.aclient.get(url, params=params or {"ucbcb": 1})
        response.raise_for_status()
        html = response.text
        load_html = json.loads(self._extract_json(html, "INNERTUBE_CONTEXT", 2, '"}},') + '"}}')
        client_context = load_html["client"]

        self.client.headers.update({
            "X-YouTube-Client-Name": "1",
            "X-YouTube-Client-Version": client_context["clientVersion"]
        })
        return html, client_context

    async def _aget_ajax_data(
        self,
        api_endpoint: str,
        api_key: str,
        next_data: dict,
        client_context: dict
    ) -> dict:
        """
        Retrieves JSON data via an AJAX POST request.

        Parameters:
            api_endpoint (str): The endpoint for the API request.
            api_key (str): API key for YouTube API.
            next_data (dict): Data required for pagination, including continuation token.
            client_context (dict): Client context obtained from the initial page.

        Returns:
            dict: JSON response from the API endpoint.
        """
        data = {
            "context": {"clickTracking": next_data["click_params"], "client": client_context},
            "continuation": next_data["token"]
        }
        response = await self.client.aclient.post(api_endpoint, params={"key": api_key}, json=data)
        response.raise_for_status()
        return response.json()

    def _extract_json(
        self,
        html: str,
        key: str,
        num_chars: int = 2,
        stop: str = '"'
    ) -> str:
        """
        Extracts JSON data from HTML based on a key.

        Parameters:
            html (str): The HTML content to search.
            key (str): The key to locate in the HTML.
            num_chars (int, optional): Number of characters to skip after the key to start extraction. Defaults to 2.
            stop (str, optional): Character where extraction ends. Defaults to '"'.

        Returns:
            str: Extracted JSON string.
        """
        pos_begin = html.find(key) + len(key) + num_chars
        pos_end = html.find(stop, pos_begin)
        return html[pos_begin:pos_end]

    def _get_next_data(
        self,
        data: dict,
        sort_by: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Retrieves the next set of pagination data.

        Parameters:
            data (dict): Current data to retrieve continuation endpoint from.
            sort_by (str, optional): Sorting option. Defaults to None.

        Returns:
            Optional[Dict]: Continuation token and click params if available; otherwise, None.
        """
        endpoint_key = "feedFilterChipBarRenderer" if sort_by and sort_by != "newest" else "continuationEndpoint"
        endpoint = next(self._search_dict(data, endpoint_key), None)
        if not endpoint:
            return None

        return {
            "token": endpoint["continuationCommand"]["token"],
            "click_params": {"clickTrackingParams": endpoint["clickTrackingParams"]}
        }

    def _search_dict(
        self,
        partial: dict,
        search_key: str
    ) -> Generator[dict, None, None]:
        """
        Searches for all matching keys in a nested dictionary.

        Parameters:
            partial (dict): The dictionary to search through.
            search_key (str): The key to look for.

        Yields:
            dict: Each matching key's value found in the dictionary.
        """
        stack = [partial]
        while stack:
            current_item = stack.pop(0)
            if isinstance(current_item, dict):
                for key, value in current_item.items():
                    if key == search_key:
                        yield value
                    else:
                        stack.append(value)
            elif isinstance(current_item, list):
                stack.extend(current_item)

    async def _yield_videos_items(
        self,
        data: dict,
        selector: str,
        limit: Optional[int],
        count: int
    ) -> AsyncGenerator[dict, None]:
        """
        Yields video items from the response data until the limit is reached.

        Parameters:
            data (dict): The JSON response data.
            selector (str): The key used to extract specific video items.
            limit (int, optional): The maximum number of videos to retrieve. Defaults to None.
            count (int): Current count of videos yielded.

        Yields:
            dict: Video items.
        """
        for result in self._get_videos_items(data, selector):
            if limit and count >= limit:
                return
            yield result

    def _get_videos_items(
        self,
        data: dict,
        selector: str
    ) -> Generator[dict, None, None]:
        """
        Extracts video items from response data.

        Parameters:
            data (dict): The JSON data received from the response.
            selector (str): Key to select video items.

        Yields:
            dict: Video items from the response data.
        """
        return self._search_dict(data, selector)

    async def aget_videos(
        self,
        url: str,
        api_endpoint: str,
        selector: str,
        limit: Optional[int] = None,
        sleep: float = 1,
        sort_by: Optional[str] = None
    ) -> AsyncGenerator[dict, None]:
        """
        Asynchronously retrieves video data from YouTube.

        Parameters:
            url (str): The YouTube page URL to retrieve data from.
            api_endpoint (str): API endpoint for further data retrieval.
            selector (str): The key used to extract specific video items.
            limit (int, optional): The maximum number of videos to retrieve. Defaults to None.
            sleep (float, optional): Time (in seconds) to sleep between requests to avoid rate limiting. Defaults to 1.
            sort_by (str, optional): Sorting order for videos. Defaults to None.

        Yields:
            dict: Information about each video.
        """
        count = 0
        next_data = None
        api_key = None
        client_context = None
        first_iteration = True

        while True:
            try:
                if first_iteration:
                    html, client_context = await self._aget_initial_data(url)
                    api_key = self._extract_json(html, "innertubeApiKey", 3)
                    data = json.loads(self._extract_json(html, "var ytInitialData = ", 0, "};") + "}")
                    next_data = self._get_next_data(data, sort_by)
                    first_iteration = False

                    if sort_by and sort_by != "newest":
                        continue
                else:
                    data = await self._aget_ajax_data(
                        api_endpoint,
                        api_key,
                        next_data,
                        client_context
                    )
                    next_data = self._get_next_data(data)

                for result in self._get_videos_items(data, selector):
                    count += 1
                    yield result
                    if limit and count >= limit:
                        return

                if not next_data:
                    break

                await asyncio.sleep(sleep)

            except httpx.HTTPStatusError as e:
                log.error(f"HTTP Error: {e}")
                break
            except Exception as e:
                log.error(f"An unexpected error occurred: {e}")
                break

        await self.client.close()

    async def aget_channel(
        self,
        channel_id: str = None,
        channel_url: str = None,
        channel_username: str = None,
        limit: Optional[int] = None,
        sleep: float = 1,
        sort_by: str = "newest",
        content_type: str = "videos"
    ) -> AsyncGenerator[dict, None]:
        """
        Asynchronously retrieves videos from a YouTube channel.

        Parameters:
            channel_id (str, optional): YouTube channel ID. Defaults to None.
            channel_url (str, optional): URL of the channel. Defaults to None.
            channel_username (str, optional): Username of the channel. Defaults to None.
            limit (int, optional): Maximum number of videos to retrieve. Defaults to None.
            sleep (float, optional): Sleep interval between requests. Defaults to 1.
            sort_by (str, optional): Sorting order for videos. Defaults to "newest".
            content_type (str, optional): Type of content to retrieve. Defaults to "videos".

        Yields:
            dict: Information about each video.
        """
        if channel_url:
            base_url = channel_url
        elif channel_id:
            base_url = f"{Domain.YOUTUBE.CHANNEL}{channel_id}"
        elif channel_username:
            base_url = f"{Domain.YOUTUBE.USER_NAME}{channel_username}"
        else:
            base_url = None

        async for video in self.aget_videos(
            f"{base_url}/{content_type}?view=0&flow=grid",
            Domain.YOUTUBE.YT_BROWSE,
            TYPE_PROPERTY_MAP[content_type],
            limit,
            sleep,
            sort_by
        ):
            yield video

    async def aget_playlist(
        self,
        playlist_id: str,
        limit: Optional[int] = None,
        sleep: float = 1
    ) -> AsyncGenerator[dict, None]:
        """
        Asynchronously retrieves videos from a YouTube playlist.

        Parameters:
            playlist_id (str): The playlist ID.
            limit (int, optional): Maximum number of videos to retrieve. Defaults to None.
            sleep (float, optional): Time interval between requests to avoid being blocked. Defaults to 1.

        Yields:
            dict: Information about each video in the playlist.
        """
        async for video in self.aget_videos(
            f"{Domain.YOUTUBE.PLAYLIST}{playlist_id}",
            Domain.YOUTUBE.YT_BROWSE,
            "playlistVideoRenderer",
            limit,
            sleep
        ):
            yield video

    async def aget_search(
        self,
        query: str,
        limit: Optional[int] = None,
        sleep: float = 1,
        sort_by: str = "relevance",
        results_type: str = "video"
    ) -> AsyncGenerator[dict, None]:
        """
        Asynchronously searches YouTube and retrieves relevant videos or other results.

        Parameters:
            query (str): Search query string.
            limit (int, optional): Maximum number of results to retrieve. Defaults to None.
            sleep (float, optional): Sleep time between requests. Defaults to 1.
            sort_by (str, optional): Sort order for the search results. Defaults to "relevance".
            results_type (str, optional): Type of results to retrieve ("video", "channel", "playlist", or "movie"). Defaults to "video".

        Yields:
            dict: Information about each search result.
        """
        param_string = f"CA{SORT_BY_VALUES[sort_by]}SAhA{RESULTS_TYPE_VALUES[results_type][0]}"

        async for result in self.aget_videos(
            f"{Domain.YOUTUBE.SEARCH}{query}&sp={param_string}",
            Domain.YOUTUBE.YT_SEARCH,
            RESULTS_TYPE_VALUES[results_type][1],
            limit,
            sleep
        ):
            yield result

    async def aget_video(self, video_id: str) -> dict:
        """
        Asynchronously retrieves details of a specific video.

        Parameters:
            video_id (str): The YouTube video ID.

        Returns:
            dict: Video information.
        """
        url = f"{Domain.YOUTUBE.VIDEO}{video_id}"
        html, client_context = await self._aget_initial_data(url)
        data = json.loads(self._extract_json(html, "var ytInitialData = ", 0, "};") + "}")
        return next(
            self._search_dict(
                data,
                "videoPrimaryInfoRenderer"
            )
        )