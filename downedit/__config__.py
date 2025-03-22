__all__ = ['Config', 'DE_VERSION']


CHUNK_SIZE = 1024
DE_VERSION = open('version', 'r').read().strip()


class Config:
    """
    Central configuration class that provides access to various settings via properties.
    """

    @property
    def folder(self):
        class FolderNamespace:
            @property
            def bin(self):
                return BinFolder

            @property
            def edit(self):
                return EditFolder

            @property
            def media(self):
                return MediaFolder

        return FolderNamespace()

    @property
    def file(self):
        class FileNamespace:
            @property
            def extensions(self):
                return Extensions

        return FileNamespace()


class BinFolder:
    """
    A class that provides constants for different types of bin folders.
    """
    BIN = ".bin"


class EditFolder:
    """
    A class that provides constants for different types of edits.
    """
    EDITED_VIDEO = "Edited_Video"
    EDITED_IMG = "Edited_Photo"
    EDITED_SOUND = "Edited_Sound"
    AI_Photo_Gen = "AI_Art"
    AI_Photo_Editor = "AI_Editor"


class MediaFolder:
    """
    A class that provides constants for different types of media.
    """
    YOUTUBE = "YouTube"
    TIKTOK = "Tiktok"
    DOUYIN = "Douyin"
    KUAISHOU = "Kuaishou"


class Extensions:
    """
    A class that provides constants for different types of extensions.
    """
    VIDEO = (".mp4", ".avi", ".mov", ".flv", ".wmv")
    IMAGE = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    SOUND = (".mp3", ".m4a", ".wav", ".ogg", ".wma", ".aac")


class AIContext:
    """
    A class that provides context for AI image generation.
    """
    DEFAULT = {
        "prompt": "A futuristic city skyline",
        "negative_prompt": """
            ((disfigured)), ((bad art)), ((deformed)), ((extra limbs)),
            ((close up)), ((b&w)), (((duplicate))), ((morbid)), ((mutilated)),
            ((poorly drawn hands)), ((poorly drawn face)), (((mutation))),
            ((ugly)), (((bad proportions))), (malformed limbs), ((missing arms)),
            ((missing legs)), (((extra arms))), (((extra legs))), (fused fingers),
            (too many fingers), (((long neck))), [out of frame], canvas frame,
            video game, tiling, poorly drawn feet, body out of frame, low quality,
            cropped, blurry, weird colors, blurry, extra fingers, mutated hands,
            cartoon, Photoshop,
        """
    }

    def __init__(self, config_data=None):
        """
        Initialize AIContext with either provided or default config.
        """
        self.config_data = config_data or AIContext.DEFAULT.copy()

    def get(self, key, default=None):
        """
        Retrieve a config value, or return default if not found.
        """
        return self.config_data.get(key, default)

    def set(self, key, value):
        """
        Set a config value.
        """
        self.config_data[key] = value

    def load(self, config_data):
        """
        Load a new configuration, merging with the existing one.
        """
        self.config_data.update(config_data)

    def update(self, default_data):
        """
        Update the default configuration values.
        """
        AIContext.DEFAULT.update(default_data)

    def reset(self, new_config=None):
        """
        Reset the config to the default settings or to new provided settings.
        """
        self.config_data = new_config or AIContext.DEFAULT.copy()

    def json(self):
        """
        Return the current configuration as a JSON object.
        """
        return self.config_data

    def __getitem__(self, key):
        """
        Access config values using dictionary-like access.
        """
        return self.config_data.get(key)

    def __setitem__(self, key, value):
        """
        Set config values using dictionary-like access.
        """
        self.config_data[key] = value

    def __str__(self):
        """
        String representation of the current configuration.
        """
        return str(self.config_data)

