from colorama import Fore

from .youtube import main as youtube_main
from .kuaishou import main as kuaishou_main
from .tiktok import main as tiktok_main
from .douyin import main as douyin_main
from cli.menu._banners import get_banner

from downedit.utils import (
    log,
    selector
)


def display_menu():
    banner_display, banner_msg = get_banner("VIDEO_DL")
    selector.display_banner(
        banner_display,
        banner_msg
    )

    menu_list = {
        f" Tiktok": tiktok_main,
        f" Douyin": douyin_main,
        f" Kuaishou": kuaishou_main,
        " Youtube": youtube_main,
        " Back": lambda: None,
    }

    selector.start(
        menu_options=menu_list,
        input_message=f"{Fore.YELLOW}Select Media Platform{Fore.WHITE}"
    )


def main():
    selector.run(
        display_menu
    )


if __name__ == "__main__":
    main()
