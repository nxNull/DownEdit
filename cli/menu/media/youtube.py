from colorama import Fore

from cli.menu._banners import get_banner
from downedit.platforms import Youtube
from downedit.utils import (
    log,
    selector
)


def main():
    banner_display, banner_msg = get_banner("YOUTUBE_DL")
    selector.display_banner(
        banner_display,
        banner_msg
    )

    channel = input(f"{Fore.YELLOW}Enter Channel Url:{Fore.WHITE} ")
    video_type = selector.select_menu(
        message=f"{Fore.YELLOW}Select Video Type:{Fore.WHITE}",
        choices={
            " Videos": "videos",
            " Shorts": "shorts"
        }
    )

    youtube = Youtube()
    youtube.download_all_videos(
        channel_url=channel,
        video_type=video_type.lower().lstrip()
    )


if __name__ == "__main__":
    main()