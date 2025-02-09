import re
import uuid

from typing import Union, Generator, Optional
from pathlib import Path

from .. import (
    CHUNK_SIZE,
    EditFolder,
    MediaFolder
)

class ResourceError(Exception):
    """
    Exception class for ResourceUtil errors
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class ResourceUtil:
    """
    A utility class for managing folders and files.
    """

    def __init__(self, folder_root: Union[str, Path] = ".") -> None:
        """
        Initializes the ResourceUtil object with the specified folder root.

        Args:
            folder_root (str | Path): The base folder path for file operations.
        """
        self.folder_root = Path(folder_root).resolve()

    def folder(self, folder_root: Union[str, Path], directory_name: str) -> Path:
        """
        Creates a folder if it does not exist.

        Args:
            folder_path (str | Path): The folder path to create.

        Returns:
            Path: The created or existing folder path.
        """
        folder_path = Path(folder_root) / directory_name
        folder_path = folder_path.resolve()
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path

    @staticmethod
    def validate_folder(folder_path: Union[str, Path]) -> Path:
        """
        Validates if a folder exists.

        Args:
            folder_path (str | Path): The folder path to validate.

        Returns:
            Path: The folder path if it exists.

        Raises:
            ResourceError: If the folder does not exist.
        """
        folder_path = Path(folder_path).resolve()
        if not folder_path.exists() or not folder_path.is_dir():
            raise ResourceError(f"Folder does not exist: {folder_path}")
        return folder_path

    @classmethod
    def create_folder(cls, folder_type: str) -> str:
        """
        Creates a folder based on the specified type and returns its absolute path.

        Args:
            folder_type (str): The type of folder to create.
            - Options: "EDITED_VIDEO", "EDITED_IMG", "EDITED_SOUND", "AI_Photo_Gen", "AI_Photo_Editor"

        Returns:
            str: The absolute path of the created folder.
        """
        folder_root = cls().folder_root

        if hasattr(EditFolder, folder_type):
            folder_name = getattr(EditFolder, folder_type)
        elif hasattr(MediaFolder, folder_type):
            folder_name = getattr(MediaFolder, folder_type)
        else:
            raise ValueError(f"Invalid folder type: {folder_type}")

        return cls.folder(folder_root, folder_name)

    @classmethod
    def get_folder_path(cls, folder_root: str, directory_name: str) -> str:
        """
        Gets or creates a subfolder within the root folder.

        Args:
            folder_name (str): The subfolder name.

        Returns:
            str: The absolute path of the subfolder.
        """
        return cls.folder(folder_root, directory_name)

    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> Optional[tuple]:
        """
        Retrieves file name, extension, and size.

        Args:
            file_path (str | Path): The file path.

        Returns:
            tuple | None: Tuple of (name, extension, size) or None if file does not exist.
        """
        file_path = Path(file_path)
        if not file_path.exists() or not file_path.is_file():
            return None
        return file_path.stem, file_path.suffix, file_path.stat().st_size

    @staticmethod
    def get_file_list(
        directory: Union[str, Path],
        extensions: Optional[Union[str, tuple]] = None
    ) -> list:
        """
        Lists files in a directory filtered by extension.

        Args:
            directory (str | Path): The directory to search.
            extensions (str | tuple, optional): File extensions to filter by.

        Returns:
            list: List of file paths.
        """
        directory = Path(directory).resolve()
        if extensions:
            if isinstance(extensions, str):
                extensions = [extensions]
            extensions = [ext.lower() for ext in extensions]

        return [
            file for file in directory.rglob("*")
            if file.is_file() and (not extensions or file.suffix.lower() in extensions)
        ]

    @staticmethod
    def get_file_list_yield(
        directory: Union[str, Path],
        extensions: Optional[Union[str, tuple]] = None
    ) -> Generator[Path, None, None]:
        """
        Yields files in a directory filtered by extension.

        Args:
            directory (str | Path): The directory to search.
            extensions (str | tuple, optional): File extensions to filter by.

        Yields:
            Path: File paths.
        """
        directory = Path(directory).resolve()
        if extensions:
            if isinstance(extensions, str):
                extensions = [extensions]
            extensions = [ext.lower() for ext in extensions]

        for file in directory.rglob("*"):
            if file.is_file() and (not extensions or file.suffix.lower() in extensions):
                yield file

    @staticmethod
    def get_output_file(
        folder_path: Union[str, Path],
        file_name: str,
        file_extension: str
    ) -> Path:
        """
        Constructs an output file path.

        Args:
            folder_path (str | Path): Folder to save the file.
            file_name (str): The file name.
            file_extension (str): The file extension.

        Returns:
            Path: The output file path.
        """
        folder_path = Path(folder_path).resolve()
        return folder_path / f"{file_name}{file_extension}"

    @staticmethod
    def trim_filename(filename: Union[str, Path], max_length: int = 50) -> str:
        """
        Trim the filename to fit within the specified maximum length.

        Args:
            filename (str or Path): The full filename.
            max_length (int): The maximum number of characters to display.

        Returns:
            str: The trimmed filename.
        """
        filename = str(filename)
        if len(filename) <= max_length: return filename

        trim_length = (max_length - 3) // 2
        return f"{filename[:trim_length]}...{filename[-trim_length:]}"

    @staticmethod
    def normalize_filename(
        folder_location: str,
        file_name: str,
        file_extension: str
    ) -> str:
        """
        Normalizes a filename by removing special characters and handling empty names.

        Args:
            folder_location (str): The folder location for the file.
            file_name (str): The original filename.
            file_extension (str): The extension of the file (including the dot, e.g., ".mp4", ".jpeg").

        Returns:
            str: The normalized filename with a path.
        """
        cleaned_name = re.sub(r'["*<>?\\|/:]', '', file_name).strip()
        if not cleaned_name: cleaned_name = str(uuid.uuid4())

        dir_path = Path(folder_location) / (cleaned_name + file_extension)

        counter = 1
        while dir_path.exists():
            dir_path = Path(folder_location) / f"{counter}{cleaned_name}{file_extension}"
            counter += 1

        return str(dir_path)

    @staticmethod
    def read_or_create_file(
        filename: Union[str, Path],
        content: str = ""
    ) -> str:
        """
        Reads a .txt or .env file, and if it doesn't exist, creates a new one with the specified content.

        Args:
            filename (str | Path): The name of the file to read or create.
            content (str): The content to write to the file if it doesn't exist.

        Returns:
            str: The content of the file.
        """
        file_path = Path(filename).resolve()
        if not file_path.exists():
            with open(file_path, 'w') as file:
                file.write(content)

        with open(file_path, 'r') as file:
            return file.read()
