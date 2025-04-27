import sys

from colorama       import Fore, Back

from cli.menu.chat   import chat           as chat
from cli.menu.media  import media          as video_dl
from cli.menu.images import ai_gen_image   as ai_img_gen
from cli.menu.images import ai_edit_image  as ai_img_editor
from cli.menu.images import editor         as image_editor
from cli.menu.sounds import editor         as sound_editor
from cli.menu.videos import editor         as video_editor

from downedit        import DE_VERSION
from downedit.utils  import (
    log,
    pc_info,
    selector
)

def display_banner():
    """
    Display the banner of the application
    """
    banner_display = f"""
    {Fore.MAGENTA}██████╗░███████╗{Back.RESET}  {Back.RED}{Fore.BLACK}nxNull@GitHub - DownEdit v{DE_VERSION}{Fore.RESET}{Back.RESET}
    {Fore.MAGENTA}██╔══██╗██╔════╝{Back.RESET}  {Fore.WHITE}----------------------------------{Back.RESET}
    {Fore.MAGENTA}██║░░██║█████╗░░{Back.RESET}  {Fore.WHITE}OS : {Fore.YELLOW}{pc_info["OS"]}, {pc_info["USER"]}{Fore.RESET}
    {Fore.MAGENTA}██║░░██║██╔══╝░░{Back.RESET}  {Fore.WHITE}CPU: {Fore.YELLOW}{pc_info["CPU"]}{Fore.RESET}
    {Fore.MAGENTA}██████╔╝███████╗{Back.RESET}  {Fore.WHITE}RAM: {Fore.YELLOW}{pc_info["RAM"]:.3f} GB{Fore.RESET}
    {Fore.MAGENTA}╚═════╝░╚══════╝{Back.RESET}  {Fore.WHITE}GPU: {Fore.YELLOW}{pc_info["GPU"]}{Fore.RESET}
    """
    banner_msg = """Use arrow key and enter to select the options"""
    return banner_display, banner_msg

def display_menu():
    banner_display, banner_msg = display_banner()
    selector.display_banner(
        banner_display,
        banner_msg, title=" - Main Menu"
    )
    available_tools = {
        f" ChatDE"                              : chat.main,
        f" Download Video"                      : video_dl.main,
        f" Edit Video"                          : video_editor.main,
        f" AI Edit Video {Fore.RED}(Soon)"      : lambda: None,
        " Edit Photo"                           : image_editor.main,
        f" AI Edit Photo"                       : ai_img_editor.main,
        f" Edit Sound"                          : sound_editor.main,
        f" AI Edit Sound {Fore.RED}(Soon)"      : lambda: None,
        f" AI-Generative Image"                 : ai_img_gen.main,
        f" AI-Generative Video {Fore.RED}(Soon)": lambda: None,
        f" AI-Generative Music {Fore.RED}(Soon)": lambda: None,
        " Exit"                                 : lambda: sys.exit(0)
    }
    return selector.start(
        menu_options=available_tools,
        input_message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}"
    )

def run():
    # while True:
    #     selector.running = True
    #     try:
            display_menu()
        # except Exception as e:
        #     log.error(str(e)[:80])
        #     log.pause()
        # except KeyboardInterrupt:
        #     log.debug("Skipping the process..")

if __name__ == "__main__":
    run()