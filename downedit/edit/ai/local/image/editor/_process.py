from typing import Dict, Generator, List

from . import OperationFactory

from downedit.edit.ai.local.image.editor._task import AIImageTask
from downedit.edit.ai.local.image.editor._editor import AIImageEditor
from downedit.__config__ import Extensions
from downedit.utils import ResourceUtil
from downedit.edit.base import Handler
from downedit.edit.process import Process

class AIImgEditProcess(Process):
    def __init__(
        self,
        tool: str,
        process_folder: str,
        batch_size: int = 5,
        **kwargs
    ):
        self._tool = tool
        super().__init__(tool, process_folder, batch_size, **kwargs)

    def _generate_file_paths(self, process_folder: str) -> Generator[str, None, None]:
        """
        Yields input image paths.
        """
        return ResourceUtil.get_file_list_yield(
            directory=process_folder,
            extensions=Extensions.IMAGE
        )

    def _get_output_folder(self, tool: str) -> str:
        """
        Gets the output folder path for edited images.
        """
        return ResourceUtil.get_folder_path(
            folder_root=ResourceUtil.create_folder(folder_type="AI_Photo_Editor"),
            directory_name=tool.lstrip()
        )

    def _init_operations(self, **kwargs) -> Handler:
        """
        Initializes the image operations based on the selected tool.
        """
        _remove_bg         = OperationFactory.create("rm_bg")
        return Handler({
            " Remove Background"  : _remove_bg,
        })

    def _get_task(self) -> AIImageTask:
        """
        Gets the image task.
        """
        return AIImageTask()

    def _create_editor(self, media_path: str) -> AIImageEditor:
        """
        Creates an ImageEditor object.
        """
        return AIImageEditor(media_path)

    @staticmethod
    def get_tools() -> Dict[str, Dict[str, type]]:
        """
        Get the available image editing tools.
        """
        return {
            " Remove Background"  : {}
        }