import os

from typing import Optional
from dotenv import load_dotenv, find_dotenv
from downedit.utils import ResourceUtil


__all__ = ['AIConfig']


class AIConfig:
    """
    Configuration manager for AI provider settings and API keys.
    """
    DEFAULT_CONTENT = """
    # Select the provider you want to use
    USE_PROVIDER=

    # Input OpenAI API Key. Get: https://duck.ai/
    DUCK_API_KEY=

    # Input OpenAI API Key. Get: https://platform.openai.com/settings/organization/api-keys
    OPENAI_API_KEY=

    # Input xAI API Key. Get: https://x.ai/api
    XAI_API_KEY=

    # Input DeepSeek API Key. Get: https://platform.deepseek.com/api_keys
    DEEPSEEK_API_KEY=

    # Input Google API Key. Get: https://aistudio.google.com/apikey
    GOOGLE_API_KEY=
    """

    def __init__(self):
        """
        Initializes the environment variables and AIConfig instance.
        """
        load_dotenv(find_dotenv())

    @staticmethod
    def get_provider_name() -> str:
        """
        Returns the active provider name from environment variables.
        """
        return os.getenv("USE_PROVIDER", "deepseek")

    @staticmethod
    def get_api_key_file(
        provider_key: str = None,
        file_path: Optional[str] = "./config.txt"
    ) -> str:
        """
        Retrieves the API key for a provider from the environment or file.
        """
        if not provider_key:
            provider_key = AIConfig.get_provider_name()

        if provider_key in os.environ:
            return os.getenv(provider_key)

        file_content = ResourceUtil.read_or_create_file(
            file_path,
            AIConfig.DEFAULT_CONTENT
        )

        for line in file_content.splitlines():
            if line.startswith(provider_key):
                return line.split('=', 1)[1].strip()

        return ""

    @staticmethod
    def get_provider_config(provider_name: str) -> dict:
        """
        Retrieves configuration for a specified provider.
        """
        return AIConfig.all_provider_configs().get(provider_name, {})

    @staticmethod
    def get_api_key(provider_name: str = None, dynamic_api_key: Optional[str] = None) -> str:
        """
        Retrieves the API key for a specific provider.
        """
        if not provider_name:
            provider_name = AIConfig.get_provider_name()

        if dynamic_api_key:
            return dynamic_api_key

        return os.getenv(f"{provider_name.upper()}_API_KEY", "")

    @staticmethod
    def get_provider_base_url(provider_name: str) -> str:
        """
        Retrieves the base URL for a specific provider.
        """
        provider_configs = AIConfig.get_provider_config(provider_name)
        return provider_configs.get("base_url", "")

    @staticmethod
    def all_provider_configs():
        """
        The configuration of the services that are used in the application.

        Available services:
            - duckai: To get the API key for duckai, please visit the respective service's website.
                - api_key: https://duckduckgo.com/duckchat/v1/chat
            - openai: To get the API key for openai, please visit the respective service's website.
                - api_key: https://platform.openai.com/settings/organization/api-keys
            - xai: To get the API key for xai, please visit the respective service's website.
                - api_key: https://x.ai/api
            - deepseek: To get the API key for deepseek, please visit the respective service's website.
                - api_key: https://platform.deepseek.com/api_keys.
            - google: To get the API key for google, please visit the google's website.
                - api_key: https://aistudio.google.com/apikey.

        Returns:
            dict: The configuration of the services.
        """
        service = {}

        service["duckai"] = {}
        service["duckai"]["api_key"] = os.getenv("DUCK_API_KEY", "inaccessible cardinal")
        service["duckai"]["base_url"] = "https://duckduckgo.com/duckchat/v1/chat"
        service["duckai"]["status_url"] = "https://duckduckgo.com/duckchat/v1/status"
        service["duckai"]["country_url"] = "https://duckduckgo.com/country.json"
        service["duckai"]["models"] = [
            "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "claude-3-haiku-20240307"
        ]

        service["openai"] = {}
        service["openai"]["api_key"] = os.getenv("OPENAI_API_KEY", "")
        service["openai"]["base_url"] = "https://api.openai.com/v1/chat/completions"
        service["openai"]["models"] = []

        service["xai"] = {}
        service["xai"]["api_key"] = os.getenv("XAI_API_KEY", "")
        service["xai"]["base_url"] = "https://api.x.ai/v1/chat/completions"
        service["xai"]["models"] = []

        service["deepseek"] = {}
        service["deepseek"]["api_key"] = os.getenv("DEEPSEEK_API_KEY", "")
        service["deepseek"]["base_url"] = "https://api.deepseek.com/chat/completions"
        service["deepseek"]["models"] = []

        service["google"] = {}
        service["google"]["api_key"] = os.getenv("GOOGLE_API_KEY", "")
        service["google"]["base_url"] = "https://generativelanguage.googleapis.com/v1beta/"
        service["google"]["models"] = [
            "gemini-1.5-flash"
        ]

        return service