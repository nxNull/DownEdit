
from abc import ABC, abstractmethod

from downedit.edit.base import Operation
from ._generator import GenerativeImageAI


class AIImgGenOperation(Operation, ABC):
    """
    Abstract class for ai image operations.
    """
    @abstractmethod
    async def _run(self, gen: GenerativeImageAI):
        pass

    async def handle(self, gen: GenerativeImageAI, output_suffix: str) -> str:
        """
        Handles the operation and updates the output suffix.

        Args:
            gen (GenerativeImageAI): The image generator instance.
            output_suffix (str): The current output suffix.

        Returns:
            str: The updated output suffix.
        """
        _img_name, _img_url = await self._run(gen)
        return (
            _img_url,
            f"{_img_name}{output_suffix}{self.suffix}"
        )

class AIImgGenAPI(AIImgGenOperation):
    """
    Abstract class for ai image operations that use an API.
    """
    def __init__(self):
        super().__init__(
            name="DownEdit Provider",
            function=self._run,
            suffix="_ai_gen"
        )

    async def _run(self, gen: GenerativeImageAI):
        fileInfo = await gen.generate()
        fileData = fileInfo.get("data")
        fileId = fileData.get("fileId")
        fileUrl = fileData.get("url")
        return (
            f"{fileId}",
            fileUrl
        )