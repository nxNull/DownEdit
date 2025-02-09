from colorama import Fore

from downedit.cli.menu._banners import get_banner
from downedit.platforms import KuaiShou
from downedit.utils import (
    log,
    selector
)


def main():
    banner_display, banner_msg = get_banner("KUAISHOU_DL")
    selector.display_banner(
        banner_display,
        banner_msg
    )
    user = input(f"{Fore.YELLOW}Enter User Link:{Fore.WHITE} ")
    # Is Working with cookies is a bit tricky. Currently we'll just ask the user to input it
    cookies = input(f"{Fore.YELLOW}Enter Cookies:{Fore.WHITE} ")
    kuaishou = KuaiShou(user=user, cookies=cookies)
    kuaishou.download_all_videos()

if __name__ == "__main__":
    main()