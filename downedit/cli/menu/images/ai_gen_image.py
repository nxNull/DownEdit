import time

from colorama import Fore

from .. import get_banner
from downedit.edit.ai.cloud.image import AIImgGenProcess
from downedit.utils import (
    log,
    selector
)


def cloud_ai_generator():
    user_prompt = input(
        f"{Fore.YELLOW}Enter prompt:{Fore.WHITE} "
    )
    image_sizes = {
        " 512x512": "512x512",
        " 512x768": "512x768",
        " 768x512": "768x512",
    }
    selected_size = selector.select_menu(
        message=f"{Fore.YELLOW}Image Size{Fore.WHITE}",
        choices=image_sizes
    ).strip()
    image_amounts = input(
        f"{Fore.YELLOW}Enter amount of images (Max: 99):{Fore.WHITE} "
    )
    with AIImgGenProcess(
        context={
            "prompt": user_prompt,
            "size": selected_size
        },
        amount= min(int(image_amounts) if image_amounts.isdigit() else 1, 99),
        batch_size=5,
        **{}
    ) as ai_image_gen_process:
        ai_image_gen_process.start()

def local_ai_generator():
    return None

def display_menu():
    banner_display, banner_msg = get_banner("AI_IMAGE_GENERATOR")
    selector.display_banner(
        banner_display,
        banner_msg, "- ai generative"
    )
    available_tools = {
        f" Cloud"                  : lambda: None,
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
