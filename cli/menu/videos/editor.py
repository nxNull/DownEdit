import multiprocessing
import time

from colorama import Fore

from cli.menu._banners import get_banner
from downedit import Video
from downedit.utils import (
    log,
    selector,
    ResourceUtil
)


def main():
    max_cpu_cores = multiprocessing.cpu_count()
    banner_display, banner_msg = get_banner("VIDEO_EDITOR")
    selector.display_banner(banner_display, banner_msg, "- Video editor")
    available_tools = Video.get_tools()
    video_presets = {
        " Ultrafast": "ultrafast",
        " Superfast": "superfast",
        " Veryfast" : "veryfast",
        " Faster"   : "faster",
        " Fast"     : "fast",
        " Medium"   : "medium",
        " Slow"     : "slow",
    }
    cpu_cores_choices = [
        str(i) for i in range(
            1,
            max_cpu_cores + 1
        )
    ]
    user_folder = ResourceUtil.validate_folder(
        folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
    )
    selected_tool = selector.select_menu(
        message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}",
        choices=available_tools
    )
    video_params = selector.get_tool_input(
        available_tools,
        selected_tool
    )
    selected_presets = selector.select_menu(
        message=f"{Fore.YELLOW}Video Preset{Fore.WHITE}",
        choices=video_presets
    ).lower().lstrip()
    selected_threads = selector.select_menu(
        message=f"{Fore.YELLOW}CPU Threads (Max: {max_cpu_cores}){Fore.WHITE}", 
        choices=cpu_cores_choices
    )
    selected_batch = input(
        f"{Fore.YELLOW}Batch Size (Max: 10):{Fore.WHITE} "
    )
    with Video(
        tool=selected_tool,
        process_folder=user_folder,
        batch_size= min(int(selected_batch) if selected_batch.isdigit() else 1, 10),
        **video_params
    ) as video_process:
        video_process.start(
            threads=int(selected_threads),
            preset=selected_presets
        )

if __name__ == "__main__":
    main()