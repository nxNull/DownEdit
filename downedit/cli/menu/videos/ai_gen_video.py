import time

from colorama import Fore

from downedit.cli.menu._banners import get_banner
from downedit.utils import (
    log,
    selector
)

def cloud_ai_generator():
    return None

def local_ai_generator():
    return None

def display_menu():
    banner_display, banner_msg = get_banner("AI_VIDEO_GENERATOR")
    selector.display_banner(
        banner_display,
        banner_msg, "- ai generative"
    )
    available_tools = {
        f" Cloud {Fore.RED}(Soon)" : lambda: None,
        f" Local {Fore.RED}(Soon)" : lambda: None,
        f" Back"                   : lambda: None,
    }
    return selector.start(
        menu_options=available_tools,
        input_message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}"
    )

def main():
    selector.run(
        display_menu
    )

if __name__ == "__main__":
    main()
