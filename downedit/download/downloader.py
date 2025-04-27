import asyncio
import aiofiles
import httpx

from typing import Any, List
from aiofiles.os import path as aiopath

from downedit.service import Client
from downedit.utils import (
    console,
    column,
    ResourceUtil,
    log
)

CHUNK_SIZES = [
    (10 * 1024, 64 * 1024),
    (1 * 1024 * 1024, 256 * 1024),
    (10 * 1024 * 1024, 1 * 1024 * 1024),
    (100 * 1024 * 1024, 10 * 1024 * 1024),
]

class Downloader:
    """
    A class to handle file downloads from the internet.
    """

    def __init__(self, service: Client):
        self.service = service
        self.download_tasks: List[asyncio.Task] = []
        self.task_progress = console().progress_bar(
            column_config=column().download()
        )

    def _get_chunk_size(self, file_size: int) -> int:
        """
        Determines the optimal chunk size based on file size.
        """
        for limit, size in CHUNK_SIZES:
            if file_size < limit:
                return size
        return 5 * 1024 * 1024

    async def _get_content_length(self, content_url: str, headers: dict = None) -> int:
        """
        Retrieves the content length of a file from the given URL.
        """
        try:
            async with self.service.aclient.stream(
                method="GET",
                url=content_url,
                headers=headers,
                follow_redirects=True,
                timeout=10
            ) as response:
                response.raise_for_status()
                return int(response.headers.get("Content-Length", 0))
        except Exception as e:
            log.error(f"Failed to retrieve content length: {e}")
            return 0

    async def _download_part(self, task_id, url: str, headers: dict, start: int, end: int, output_file: str):
        """
        Downloads a part of the file within the specified byte range.
        """
        range_headers = {**headers, "Range": f"bytes={start}-{end}"}
        async with self.service.aclient.stream(
            "GET",
            url,
            headers=range_headers,
            follow_redirects=True
        ) as response:
            response.raise_for_status()
            async with aiofiles.open(output_file, mode="r+b") as file:
                await file.seek(start)
                async for chunk in response.aiter_bytes():
                    await file.write(chunk)
                    await self.task_progress.update_task(
                        task_id,
                        progress_increment=len(chunk)
                    )

    async def _initialize_download_task(self, file_url: str, file_media: Any, service_step: tuple) -> tuple:
        """
        Initializes a download task, setting up progress bar tracking.
        """
        file_output, file_name = file_media
        start_step, *_ = service_step
        task_id = await self.task_progress.add_task(
            description=start_step,
            file_name=ResourceUtil.trim_filename(file_name, 40).ljust(40),
            start=True,
            current_state="idle",
        )

        if await aiopath.exists(file_output):
            await self.task_progress.update_task(
                task_id=task_id,
                description="Skipping",
                total=1,
                completed=1,
                new_state="success",
            )
            return None, None, None

        await self.task_progress.update_task(task_id, new_state="starting")
        return task_id, file_output, file_name

    async def add_file(
        self,
        file_url: str,
        file_media: Any,
        service_step: tuple = ("Download", "Downloading", "Downloaded"),
        num_parts: int = 4,
        small_file_threshold: int = 10 * 1024 * 1024,
    ):
        """
        Adds a file to the download queue and configures the task.

        Args:
            file_url: The URL of the file to download.
            file_media: The file output and metadata.
            service_step: Progress step descriptions.
            num_parts: Number of parts for multipart download.
            small_file_threshold: Size threshold for small file optimization.
        """
        task_id, file_output, file_name = await self._initialize_download_task(
            file_url,
            file_media,
            service_step
        )
        if task_id is None:
            return

        content_length = await self._get_content_length(
            file_url,
            self.service.headers
        )
        if content_length == 0:
            return await self.task_progress.update_task(
                task_id, new_state="failure", still_visible=True
            )

        download_task = asyncio.create_task(
            self.download_file(
                service_step=service_step,
                task_id=task_id,
                file_name=file_name,
                file_url=file_url,
                file_output=file_output,
                num_parts=2 if content_length < small_file_threshold else num_parts,
                content_length=content_length
            )
        )

        # download_task = asyncio.create_task(
        #     self._download_single_file(
        #         service_step=service_step,
        #         task_id=task_id,
        #         file_name=file_name,
        #         file_url=file_url,
        #         file_output=file_output,
        #         content_length=content_length
        #     )
        #     if content_length < small_file_threshold
        #     else self.download_file(
        #         service_step=service_step,
        #         task_id=task_id,
        #         file_name=file_name,
        #         file_url=file_url,
        #         file_output=file_output,
        #         num_parts=num_parts,
        #         content_length=content_length
        #     )
        # )
        self.download_tasks.append(download_task)

    async def _download_single_file(
        self,
        service_step: tuple,
        task_id,
        file_name: str,
        file_url: str,
        file_output: str,
        content_length: int = 0,
    ):
        """
        Downloads a small file in a single stream.
        """
        _, working_step, end_step = service_step
        headers = self.service.headers

        async with self.service.semaphore:
            await self.task_progress.update_task(
                task_id,
                new_state="downloading"
            )
            try:
                async with self.service.aclient.stream(
                    "GET",
                    file_url,
                    headers=headers,
                    follow_redirects=True
                ) as response:
                    response.raise_for_status()
                    await self.task_progress.update_task(
                        task_id,
                        new_total=content_length
                    )

                    async with aiofiles.open(file_output, mode="wb") as file:
                        async for chunk in response.aiter_bytes():
                            await file.write(chunk)
                            await self.task_progress.update_task(
                                task_id,
                                progress_increment=len(chunk)
                            )
            except Exception as e:
                # log.error(f"Error during {working_step}: {e}")
                return await self.task_progress.update_task(
                    task_id, new_state="failure", still_visible=True
                )

        await self.task_progress.update_task(
            task_id,
            new_state="success",
            still_visible=True
        )

    async def download_file(
        self,
        service_step: tuple,
        task_id,
        file_name: str,
        file_url: str,
        file_output: str,
        num_parts: int = 4,
        content_length: int = 0,
    ):
        """
        Downloads a file using multiple parts to improve speed.
        """
        _, working_step, end_step = service_step
        headers = self.service.headers

        async with self.service.semaphore:
            if content_length == 0:
                return await self.task_progress.update_task(
                    task_id, new_state="failure", still_visible=True
                )

            await self.task_progress.update_task(
                task_id,
                new_total=content_length
            )
            async with aiofiles.open(file_output, mode="wb") as file:
                await file.seek(content_length - 1)
                await file.write(b'\0')

            part_size = content_length // num_parts
            download_tasks = [
                self._download_part(
                    task_id,
                    file_url,
                    headers,
                    part * part_size,
                    min((part + 1) * part_size - 1, content_length - 1),
                    file_output
                )
                for part in range(num_parts)
            ]

            try:
                for task in asyncio.as_completed(download_tasks):
                    await task
                    await self.task_progress.update_task(task_id)
            except Exception as e:
                # log.error(f"Error during {working_step}: {e}")
                return await self.task_progress.update_task(
                    task_id, new_state="failure", still_visible=True
                )

        await self.task_progress.update_task(task_id, new_state="success", still_visible=True)

    async def execute(self):
        """
        Executes all queued download tasks concurrently.
        """
        await asyncio.gather(*self.download_tasks)
        self.download_tasks.clear()

    async def close(self):
        """
        Closes resources and cleans up tasks.
        """
        try:
            if self.service.client:
                self.service.client.close()
            if self.service.aclient:
                await self.service.aclient.aclose()
        except Exception as e:
            log.error(f"Error during resource cleanup: {e}")

    async def __aenter__(self):
        """
        Enters the context manager.
        """
        self.task_progress.__enter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the context manager.
        """
        self.task_progress.__exit__(exc_type, exc_val, exc_tb)
        await self.close()