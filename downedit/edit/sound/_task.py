import asyncio
import os

from downedit.edit.base import Task
from downedit.utils import (
    console,
    column,
    ResourceUtil
)


class SoundTask(Task):
    """
    Task to be performed on sound editor based on the selected operation.
    """
    def __init__(self):
        self.img_tasks = []
        self.task_progress = console().progress_bar(
            column_config=column().edit()
        )

    async def init_progress(self):
        """
        Initializes the progress bar.
        """
        self.task_progress.start()

    async def add_task(
        self,
        operation_function,
        operation_media,
    ) -> None:
        """
        Adds a task to the queue and updates the progress bar.

        Args:
            operation_function: The asynchronous function to perform the sound edit.
            operation_sound: The identifier for the sound.
            output_suffix: The suffix to add to the edited sound.
            output_folder: The folder to save the edited sound.
        """
        file_output, file_name, file_size = operation_media
        units_done = (
            file_size
            if os.path.exists(file_output)
            else (os.path.getsize(file_output) if os.path.isfile(file_output) else 0)
        )
        task_id = await self.task_progress.add_task(
            description="Edit",
            total_units=file_size,
            units_done=units_done,
            file_name=ResourceUtil.trim_filename(file_name, 40).ljust(40),
            current_state="idle"
        )
        if units_done == file_size:
            await self.task_progress.update_task(
                task_id=task_id,
                new_description="Done",
                new_state="success"
            )
        else:
            edit_task = asyncio.create_task(
                self.task_wrapper(
                    task_id,
                    operation_function,
                    file_size
                )
            )
            self.img_tasks.append(edit_task)

    async def end_progress(self):
        """
        Ends the progress bar.
        """
        self.task_progress.end()

    async def task_wrapper(self, task_id, operation_function, completed):
        """
        Wrapper function for the task to be performed on the sound editor.
        """
        await self.task_progress.update_task(
            task_id,
            new_state="starting"
        )
        await asyncio.to_thread(operation_function)
        await self.task_progress.update_task(
            task_id=task_id,
            new_completed=completed,
            new_description="Done",
            new_state="success"
        )

    async def execute(self):
        """
        Executes all queued sound editing tasks concurrently.
        """
        with self.task_progress:
            await asyncio.gather(*self.img_tasks)
            await asyncio.sleep(0.1)

    async def close(self):
        """
        Clears the list of queued tasks.
        """
        self.img_tasks.clear()

    async def __aenter__(self):
        """
        Enter the context manager
        """
        self.task_progress.__enter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context manager
        """
        self.task_progress.__exit__(exc_type, exc_val, exc_tb)