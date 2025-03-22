import asyncio
from colorama import Fore

from cli.menu._banners import get_banner
from downedit.agents import SIMA
from downedit.utils import (
    log,
    selector
)


def chat():
    """
    Chat function for interacting with AI agents.
    """
    sima = SIMA()

    absolute_agent = sima.create_agent(
        agent_type="cloud",
        model="o3-mini",
    )
    response = sima.instruction(
        absolute_agent,
        "Hello"
    )
    
    print(f"{Fore.CYAN}AI{Fore.WHITE}: {response.get('message', 'Hello! How can I assist you today?')}")

    while True:
        user_input = input(f"{Fore.YELLOW}You{Fore.WHITE}: ")

        if user_input.lower() in ["exit", "quit", "q", ""]:
            break

        response = sima.instruction(
            absolute_agent,
            user_input
        )

        log.debug(
            f"Response: {response}"
        )

        print(f"{Fore.CYAN}AI{Fore.WHITE}: {response.get('message', '')}")

        sima.run(
            absolute_agent,
            response.get('tools', [])
        )

def main():
    banner_display, banner_msg = get_banner("CHAT_DE")

    selector.display_banner(
        banner_display,
        banner_msg
    )

    chat()

if __name__ == "__main__":
    main()