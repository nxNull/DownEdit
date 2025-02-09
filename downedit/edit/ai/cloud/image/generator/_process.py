import asyncio
import time
import traceback

from downedit.edit.ai.cloud.image.generator._task import AIImgGenTask
from downedit.edit.ai.cloud.image.generator._generator import GenerativeImageAI
from downedit.edit.ai.cloud.image.generator import (
    OperationFactory,
    AIImgGenOperation
)
from downedit.edit.base import Handler
from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)

class AIImgGenProcess:
    def __init__(
        self,
        context: dict,
        amount: int,
        batch_size: int = 5,
        **kwargs
    ):
        self.context = context
        self.amount = amount
        self.batch_size = batch_size
        self.observer = Observer()
        self._output_folder = self._get_output_folder()
        self._provider = self._init_provider(**kwargs)
        self._ai = self._create_ai(self._provider, self.context)
        self._task = self._get_task()

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for edited video files.
        """
        return ResourceUtil.get_folder_path(
            folder_root=ResourceUtil.create_folder(folder_type="AI_Photo_Gen"),
            directory_name="Cloud"
        )

    def _init_provider(self, **kwargs):
        """
        Initializes the AI image generator provider.
        """
        return Handler({
            "ai_img_gen": OperationFactory.create("ai_img_gen", **kwargs)
        })

    def _get_task(self) -> AIImgGenTask:
        """
        Gets the image task.
        """
        return AIImgGenTask()

    async def _build_and_apply_providers(self, generator, output_suffix: str):
        """
        Build and apply the providers to the output suffix.

        Args:
            generator : The image generator instance.
            output_suffix (str): The current output suffix.
        Returns:
            str: The updated output suffix.
        """
        providers = self._provider._get("ai_img_gen")
        if isinstance(providers, AIImgGenOperation):
            img_url, output_suffix = await providers.handle(generator, output_suffix)
        elif isinstance(providers, list):
            for provider in providers:
                img_url, output_suffix = await provider.handle(generator, output_suffix)

        return (
            img_url,
            output_suffix
        )

    async def _generate_media(self, file_info, **ai_kwargs) -> bool:
        """
        Process a single media file.
        """
        try:
            file_name, file_extension = file_info
            gen_url, output_suffix = await self._build_and_apply_providers(self._ai, "")
            full_file = f"{file_name}{output_suffix}"

            output_file_path = ResourceUtil.get_output_file(
                self._output_folder,
                full_file,
                file_extension
            )
            await self._task.execute(
                operation_url = gen_url,
                operation_media = (output_file_path, full_file)
            )
            return True
        except Exception as e:
            log.error("Unable to generate image.")
            return False

    def _create_ai(self, _provider: AIImgGenOperation, _context: dict) -> GenerativeImageAI:
        """
        Creates an ImageEditor object.
        """
        return GenerativeImageAI(_provider, _context)

    async def start_async(self, **ai_kwargs):
        """
        Starts the asynchronous processing of media files.
        """
        start_time = time.time()
        proceed_count = 0
        log.info(f"[white]Start Generating Image ...[/]")

        for _ in range(self.amount):
            if self.observer.is_termination_signaled():
                break
            if await self._generate_media((proceed_count, ".jpg"), **ai_kwargs):
                proceed_count += 1

        elapsed_time = time.time() - start_time

        log.info(f"[white]Processed: {elapsed_time:.2f} seconds.[/]")
        log.file(f"Saved at [green]{self._output_folder}[/green]")
        log.file(f"Processed [green]{proceed_count}[/green] media files successfully.")
        log.pause()

    def start(self, **ai_kwargs):
        """
        Process the media files in the input folder synchronously.
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(self.start_async(**ai_kwargs))
        except Exception as e:
            log.error(traceback.format_exc())

    def __enter__(self):
        """
        Set up the context for image generating.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Clean up the context after media processing.
        """
        pass