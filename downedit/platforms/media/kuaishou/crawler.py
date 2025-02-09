import json
import httpx

from downedit.platforms.media.kuaishou.client import KuaiShouClient
from downedit.platforms.domain import Domain
from downedit.service import retry_async, httpx_capture_async
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    log
)

class KuaishouCrawler:
    def __init__(self, *args, **kwargs):
        self.ks_client = KuaiShouClient()
        self.cookies = kwargs.get("cookies", "")
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
    async def __crawl_user_live_videos(self, principalId: str, pcursor: str = "", cookies: str = ""):
        """
        Crawls the user information.
        """

        header = self.headers.get()
        header["Accept"] = "application/json, text/plain, */*"
        header["Connection"] = "keep-alive"
        # cookies = await self.ks_client.get_client_details()
        # get cookies from class
        header["Cookie"] = self.cookies
        header["Host"] = "live.kuaishou.com"
        header["Referer"] = Domain.KUAI_SHOU.PROFILE_URL + principalId

        response = await Client().aclient.get(
            url=Domain.KUAI_SHOU.PUBLIC_PROFILE,
            headers=header,
            params = {
                "count": 12,
                "pcursor": pcursor,
                "principalId": principalId,
                "hasMore": "true"
            }
        )

        response.raise_for_status()
        json_response = response.json()
        data = json_response.get("data", {})

        return {
            "result": data.get("result", 0),
            "pcursor": data.get("pcursor", ""),
            "videos": data.get("list", [])
        }

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
    async def __crawl_user_feed_videos(self, principalId: str, pcursor: str = "", cookies: str = ""):
        """
        Crawls the user information.
        """
        query = """
        fragment photoContent on PhotoEntity {
            __typename
            id
            duration
            caption
            originCaption
            likeCount
            viewCount
            commentCount
            realLikeCount
            coverUrl
            photoUrl
            photoH265Url
            manifest
            manifestH265
            videoResource
            coverUrls {
                url
                __typename
            }
            timestamp
            expTag
            animatedCoverUrl
            distance
            videoRatio
            liked
            stereoType
            profileUserTopPhoto
            musicBlocked
            riskTagContent
            riskTagUrl
        }

        fragment recoPhotoFragment on recoPhotoEntity {
            __typename
            id
            duration
            caption
            originCaption
            likeCount
            viewCount
            commentCount
            realLikeCount
            coverUrl
            photoUrl
            photoH265Url
            manifest
            manifestH265
            videoResource
            coverUrls {
                url
                __typename
            }
            timestamp
            expTag
            animatedCoverUrl
            distance
            videoRatio
            liked
            stereoType
            profileUserTopPhoto
            musicBlocked
            riskTagContent
            riskTagUrl
        }

        fragment feedContentWithLiveInfo on Feed {
            type
            author {
                id
                name
                headerUrl
                following
                livingInfo
                headerUrls {
                    url
                    __typename
                }
                __typename
            }
            photo {
                ...photoContent
                ...recoPhotoFragment
                __typename
            }
            canAddComment
            llsid
            status
            currentPcursor
            tags {
                type
                name
                __typename
            }
            __typename
        }

        query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {
            visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {
                result
                llsid
                webPageArea
                feeds {
                ...feedContentWithLiveInfo
                __typename
                }
                hostName
                pcursor
                __typename
            }
        }
        """

        payload = json.dumps({
            "operationName": "visionProfilePhotoList",
            "variables": {
                "userId": principalId,
                "pcursor": pcursor,
                "page": "profile"
            },
            "query": query
        }, indent=4)

        header = self.headers.get()
        header["Accept"] = "*/*"
        header["Accept-Language"] = "en-US,en;q=0.9"
        header["Content-Type"] = "application/json"
        header["Connection"] = "keep-alive"
        cookies = await self.ks_client.get_client_details(principalId)
        # log.info(f"cookies: {cookies}")
        # get cookies from class
        header["Cookie"] = cookies
        # header["Cookie"] = self.cookies
        header["Host"] = "www.kuaishou.com"
        header["Origin"] = Domain.KUAI_SHOU.KAUI_SHOU_DOMAIN
        header["Referer"] = Domain.KUAI_SHOU.FEED_PROFILE_URL + principalId
        header["Sec-Fetch-Site"] = "same-origin"

        response = await Client().aclient.post(
            url=Domain.KUAI_SHOU.DATA_URL,
            headers=header,
            data=payload
        )

        response.raise_for_status()
        json_response = response.json()
        data = json_response.get("data", {})
        profilePhotoList =  data.get("visionProfilePhotoList", {})

        return {
            "result": profilePhotoList.get("result", 0),
            "pcursor": profilePhotoList.get("pcursor", "no_more"),
            "videos": profilePhotoList.get("feeds", [])
        }

    async def fetch_user_feed_videos(self, user_id: str):
        """
        Public method to fetch user videos iteratively from feed.

        Args:
            user_id (str): The user's unique ID for Kuaishou.

        Yields:
            dict: A video metadata for the user.
        """
        try:
            pcursor = ""
            has_more = True

            while has_more:
                user_videos_data = await self.__crawl_user_feed_videos(
                    principalId=user_id,
                    pcursor=pcursor
                )
                for video in user_videos_data.get("videos", []):
                    manifest = video.get("photo", {}).get("manifest", {})
                    yield manifest["adaptationSet"][0]["representation"][0]["url"]
                pcursor = user_videos_data.get("pcursor", "")
                has_more = user_videos_data.get("result", 0) == 1 or pcursor == "no_more"

        except Exception as e:
            log.error(f"Error fetching videos for user {user_id}: {str(e)}")
            log.pause()

    async def fetch_user_live_videos(self, user_id: str):
        """
        Public method to fetch user videos iteratively from live

        Args:
            user_id (str): The user's unique ID for Kuaishou.

        Yields:
            dict: A video metadata for the user.
        """
        try:
            pcursor = ""
            has_more = True

            while has_more:
                user_videos_data = await self.__crawl_user_live_videos(
                    principalId=user_id,
                    pcursor=pcursor
                )
                for video in user_videos_data.get("videos", []):
                    yield video
                pcursor = user_videos_data.get("pcursor", "")
                has_more = user_videos_data.get("result", 0) == 1 or pcursor == "no_more"

        except Exception as e:
            log.error(f"Error fetching videos for user {user_id}: {str(e)}")
            log.pause()
