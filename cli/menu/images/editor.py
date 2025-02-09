import time

from colorama import Fore

from cli.menu._banners import get_banner
from downedit import Image
from downedit.utils import (
    log,
    selector,
    ResourceUtil
)


def main():
    banner_display, banner_msg = get_banner("IMAGE_EDITOR")
    selector.display_banner(banner_display, banner_msg, "- Photo editor")
    available_tools = Image.get_tools()

    user_folder = ResourceUtil.validate_folder(
        folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
    )
    selected_tool = selector.select_menu(
        message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}",
        choices=available_tools
    )
    image_params = selector.get_tool_input(
        available_tools,
        selected_tool
    )
    selected_batch = input(
        f"{Fore.YELLOW}Batch Size (Max: 10):{Fore.WHITE} "
    )

    with Image(
        tool=selected_tool,
        process_folder=user_folder,
        batch_size= min(int(selected_batch) if selected_batch.isdigit() else 1, 10),
        **image_params
    ) as image_process:
        image_process.start()

if __name__ == "__main__":
    main()