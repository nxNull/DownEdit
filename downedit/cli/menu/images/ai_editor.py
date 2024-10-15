
import time

from pystyle import *
from colorama import *

from .. import get_banner
from downedit.edit import AIImgEditProcess
from downedit.utils import (
    FileUtil,
    log,
    selector
)

def main():
    banner_display, banner_msg = get_banner("AI_IMAGE_EDITOR")
    selector.display_banner(banner_display, banner_msg, "- ai editor")
    available_tools = AIImgEditProcess.get_tools()
    user_folder = FileUtil.validate_folder(
        folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
    )
    selected_tool = selector.select_menu(
        message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}",
        choices=available_tools
    )
    ai_image_params = selector.get_tool_input(
        available_tools,
        selected_tool
    )
    selected_batch = input(
        f"{Fore.YELLOW}Batch Size (Max: 10):{Fore.WHITE} "
    )
    with AIImgEditProcess(
        tool=selected_tool,
        process_folder=user_folder,
        batch_size= min(int(selected_batch) if selected_batch.isdigit() else 1, 10),
        **ai_image_params
    ) as ai_image_process:
        ai_image_process.start()

if __name__ == "__main__":
    main()
