from colorama import Fore

from cli.menu._banners import get_banner
from downedit.platforms import Douyin
from downedit.utils import (
    log,
    selector
)


def main():
    banner_display, banner_msg = get_banner("DOUYIN_DL")
    selector.display_banner(
        banner_display,
        banner_msg
    )

    cookie = input(f"{Fore.YELLOW}Enter User Cookies:{Fore.WHITE} ")
    if not cookie:
        log.critical("Please Enter Cookies!")
        return

    user_link = input(f"{Fore.YELLOW}Enter User Url:{Fore.WHITE} ")
    if not user_link:
        log.critical("Please Enter User Url!")
        return

    douyin = Douyin(cookies=cookie.strip())
    douyin.download_all_videos(
        user=user_link
    )


if __name__ == "__main__":
    main()
