from typing import Dict, Generator, List

from . import OperationFactory

from ... import Extensions
from ...utils.resource import ResourceUtil

from downedit.edit.video._editor import VideoEditor
from downedit.edit.video._task import VideoTask

from ..base import Handler
from ..process import Process


class VideoProcess(Process):
    """
    Processes videos based on the selected tool.
    """
    def __init__(
        self,
        tool: str,
        process_folder: str,
        batch_size: int = 5,
        **kwargs
    ):
        super().__init__(tool, process_folder, batch_size, **kwargs)

    def _generate_file_paths(self, process_folder: str) -> Generator[str, None, None]:
        """
        Yields input video file paths.
        """
        return ResourceUtil.get_file_list_yield(
            directory=process_folder,
            extensions=Extensions.VIDEO
        )

    def _get_output_folder(self, tool: str) -> str:
        """
        Gets the output folder path for edited video files.
        """
        return ResourceUtil.get_folder_path(
            folder_root=ResourceUtil.create_folder(folder_type="EDITED_VIDEO"),
            directory_name=tool.lstrip()
        )

    def _init_operations(self, **kwargs) -> Handler:
        """
        Initializes the operations list based on the selected tool.
        This replaces the previous dictionary-based approach for better management of operation order.
        """
        _flip_edit         = OperationFactory.create("flip")
        _speed_edit        = OperationFactory.create("speed",      factor=kwargs.get("Speed", 1.0))
        _add_music_edit    = OperationFactory.create("add_music",  music_path=kwargs.get("Music", None))
        _loop_edit         = OperationFactory.create("loop",       amount=kwargs.get("Loop Amount", 1))
        _adjust_color_edit = OperationFactory.create(
            "adjust_color",
            brightness  =   kwargs.get("Brightness", 1.0),
            contrast    =   kwargs.get("Contrast", 1.0),
            saturation  =   kwargs.get("Saturation", 1.0)
        )
        return Handler({
            " Flip Horizontal"      : _flip_edit,
            " Custom Speed"         : _speed_edit,
            " Loop Video"           : _loop_edit,
            " Flip + Speed"         : [_flip_edit, _speed_edit],
            " Add Music"            : _add_music_edit,
            " Speed + Music"        : [_speed_edit, _add_music_edit],
            " Flip + Speed + Music" : [_flip_edit, _speed_edit, _add_music_edit],
            " Adjust Color"         : _adjust_color_edit
        })

    def _get_task(self) -> VideoTask:
        """
        Gets the video task.
        """
        return VideoTask()

    def _create_editor(self, media_path: str) -> VideoEditor:
        """
        Creates a VideoEditor object.
        """
        return VideoEditor(media_path)

    @staticmethod
    def get_tools() -> Dict[str, Dict[str, type]]:
        """
        Get the available video editing tools.
        """
        return {
            " Flip Horizontal"      : {},
            " Custom Speed"         : {"Speed": float},
            " Loop Video"           : {"Loop Amount": int},
            " Flip + Speed"         : {"Speed": float},
            " Add Music"            : {"Music": str},
            " Speed + Music"        : {"Speed": float, "Music": str},
            " Flip + Speed + Music" : {"Speed": float, "Music": str},
            " Adjust Color"         : {"Brightness": float, "Contrast": float, "Saturation": float},
        }