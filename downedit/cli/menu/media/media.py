import time
from colorama import Fore

from downedit.cli.menu._banners import get_banner
from downedit.platforms import (
    Douyin,
    Tiktok
)
from .youtube import main as youtube_main
from .kuaishou import main as kuaishou_main
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
    # TODO: Media Video Downloader Algorithm
    menu_list = {
        f" Tiktok  {Fore.RED}(Rework)": lambda: None,
        f" Douyin {Fore.RED}(Rework)": lambda: None,
        # f" Kuaishou {Fore.RED}(Rework)": lambda: None,
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
