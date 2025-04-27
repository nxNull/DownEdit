
class KuaishouParam:
    """
    Kuaishou parameter configuration.
    """

    def __init__(self):
        pass

    @classmethod
    def get_video_list(
        cls,
        principalId: str,
        pcursor: str = "",
        count: int = 18,
    ) -> dict:
        """
        Get the parameters for the video list request.
        """

        return {
            "operationName": "visionProfilePhotoList",
            "variables": {
                "page": "profile",
                "pcursor": pcursor,
                "userId": principalId,
            },
            "query": """
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
        }