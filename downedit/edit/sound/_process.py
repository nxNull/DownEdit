from typing import Dict, Generator, List

from . import OperationFactory

from ... import Extensions
from ...utils.resource import ResourceUtil

from downedit.edit.sound._editor import SoundEditor
from downedit.edit.sound._task import SoundTask

from ..base import Handler
from ..process import Process


class SoundProcess(Process):
    """
    Processes sounds based on the selected tool.
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
        Yields input sound file paths.
        """
        return ResourceUtil.get_file_list_yield(
            directory=process_folder,
            extensions=Extensions.SOUND
        )

    def _get_output_folder(self, tool: str) -> str:
        """
        Gets the output folder path for edited sound files.
        """
        return ResourceUtil.get_folder_path(
            folder_root=ResourceUtil.create_folder(folder_type="EDITED_SOUND"),
            directory_name=tool.lstrip()
        )

    def _init_operations(self, **kwargs) -> Handler:
        """
        Initializes the sound operations based on the selected tool.
        """
        _volume    =  OperationFactory.create("Volume", kwargs.get("Level", 0.5))
        _fade_in   =  OperationFactory.create("Fade In", kwargs.get("Fade In Duration", 2))
        _fade_out  =  OperationFactory.create("Fade Out", kwargs.get("Fade Out Duration", 2))
        return Handler({
            " Volume"   : _volume,
            " Fade In"  : _fade_in,
            " Fade Out" : _fade_out
        })

    def _get_task(self) -> SoundTask:
        """
        Gets the sound task.
        """
        return SoundTask()

    def _create_editor(self, media_path: str) -> SoundEditor:
        """
        Creates a SoundEditor object.
        """
        return SoundEditor(media_path)

    @staticmethod
    def get_tools() -> Dict[str, Dict[str, type]]:
        """
        Get the available sound editing tools.
        """
        return {
            " Volume"   : {"Level": float},
            " Fade In"  : {"Fade In Duration": float},
            " Fade Out" : {"Fade Out Duration": float},
        }