import os
import time
import inquirer

from colorama import Fore
from pystyle import Box, Center
from abc import ABC, abstractmethod

from .singleton import Singleton
from .logger import log


class UserInput(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_user_input(self, message):
        pass

    @abstractmethod
    def select_input(self, tool_selector, banner, message):
        pass


class SingleInput(UserInput):
    def get_user_input(self, message):
        return input(message)

    def select_input(self, tool_selector, banner, message):
        tool_selector.display_banner(banner, message)
        user_input = self.get_user_input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")
        if not user_input:
            log.critical("Please Enter Username!")
            return
        return user_input


class BatchInput(UserInput):
    def get_user_input(self, message):
        return input(message)

    def select_input(self, tool_selector, banner, message):
        tool_selector.display_banner(banner, message)
        file_path = self.get_user_input(f"{Fore.YELLOW}Enter File Path:{Fore.WHITE} ")
        if not file_path:
            log.critical("Please Enter File Path!")
            return
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                return lines
        except FileNotFoundError:
            log.error("File not found or could not be opened.")
            return []

class ToolSelector(metaclass=Singleton):
    def __init__(self) -> None:
        self.running = True
        self._user_input = None

    def set_user_input(self, selection: UserInput):
        self._user_input = selection

    def get_user_input(self, message):
        if self._user_input is None:
            raise ValueError("User input strategy not set")
        return self._user_input.get_user_input(message)

    def get_tool_input(self, available_tools, tool_name):
        """
        Get the function input based on the selected tool.

        Args:
            available_tools (dict): The available tools.
            tool_name (str): The selected tool.

        Returns:
            dict: The function input for the selected tool.
        """

        if tool_name not in available_tools:
            raise Exception(f"Tool '{tool_name}' not found in available tools.")

        function_input = {}
        for message, function_type in available_tools[tool_name].items():
            if not isinstance(function_type, type):
                raise Exception(f"Invalid '{function_type}' for input '{message}'.")

            prompt = f"{Fore.YELLOW}Enter {message}:{Fore.WHITE} "
            function_input[message] = function_type(input(prompt))

        return function_input

    def show_box(self, message):
        """
        Display the message in a box.

        Args:
            message (str): The message to display.

        Returns:
            String: The message in a box.
        """
        print(f'{Fore.GREEN}')
        print(Box.DoubleCube(message))

    def display_banner(self, banner, message, title=None):
        """
        Display the banner and message.

        Args:
            banner (str): The banner to display.
            message (str): The message to display.
            title (str): The title to display.

        Returns:
            None
        """
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title DownEdit {title}" if os.name == "nt" else "")
        print(Center.XCenter(banner))
        self.show_box(message)

    def select_menu(self, message, choices) -> str:
        """
        Selects an option from the menu.

        Args:
            message (str): The message to display.
            choices (list): The choices to select from.

        Returns:
            String: The selected choice.
        """
        questions = [
            inquirer.List(
                'list',
                message=message,
                choices=choices
            )
        ]
        answers = inquirer.prompt(questions)
        return answers['list']

    def execute_menu(self, selected, functions):
        """
        Executes the selected function.

        Args:
            selected (str): The selected function.
            functions (dict): The functions to execute.

        Returns:
            Function: The selected function.
        """
        if selected in functions:
            if selected == " Back":
                self.running = False
                return
            functions[selected]()

    def manual_select(
        self,
        menu_options: dict,
        banner,
        message,
    ):
        self.display_banner(banner=banner, message=message)
        question = self.select_menu(
            message=f"{Fore.YELLOW}Select Option{Fore.WHITE}",
            choices=menu_options
        )
        return question

    def selection_input(
        self,
        strategy: UserInput,
        banner,
        message
    ):
        return strategy.select_input(self, banner, message)

    def start(
        self,
        menu_options: dict,
        input_message: str,
    ) -> None:
        """
        Starts the tool selection process.

        Args:
            menu_options (dict): The menu options.
            input_message (str): The input message.

        Returns:
            None
        """
        chosen_tool = self.select_menu(
            message=input_message,
            choices=list(menu_options.keys())
        )
        self.execute_menu(
            chosen_tool,
            menu_options
        )

    def run(self, main_func, *args, **kwargs):
        """
        Run the main function.

        Args:
            main_func (function): The main function to run.
        """
        while self.running:
            try:
                main_func(*args, **kwargs)
            except Exception as e:
                log.error(str(e)[:80])
                time.sleep(0.5)
                log.pause()
            except KeyboardInterrupt:
                log.debug("Skipping the process..")

# Create an instance of the ToolSelector class.
selector = ToolSelector()