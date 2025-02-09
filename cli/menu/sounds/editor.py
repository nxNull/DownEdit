import time

from colorama import Fore

from cli.menu._banners import get_banner
from downedit import Sound
from downedit.utils import (
    log,
    selector,
    ResourceUtil
)


def main():
    banner_display, banner_msg = get_banner("SOUND_EDITOR")
    selector.display_banner(banner_display, banner_msg, "- Sound editor")
    available_tools = Sound.get_tools()
    user_folder = ResourceUtil.validate_folder(
        folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
    )
    selected_tool = selector.select_menu(
        message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}",
        choices=available_tools
    )
    sound_params = selector.get_tool_input(
        available_tools,
        selected_tool
    )
    selected_batch = input(
        f"{Fore.YELLOW}Batch Size (Max: 10):{Fore.WHITE} "
    )
    with Sound(
        tool=selected_tool,
        process_folder=user_folder,
        batch_size= min(int(selected_batch) if selected_batch.isdigit() else 1, 10),
        **sound_params
    ) as sound_process:
        sound_process.start()

if __name__ == "__main__":
    main()