from asyncio import Lock
from typing import Optional, Dict
from rich.spinner import Spinner
from rich.progress import (
    Progress as RichProgress,
    TaskID,
    Task,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    DownloadColumn,
    TransferSpeedColumn,
    ProgressColumn,
    SpinnerColumn,
    TimeElapsedColumn
)

from .singleton import Singleton


class SpinnerColumn(ProgressColumn):
    """
    Customized spinner columns for progress display
    (Usage Example): python -m rich.spinner
    """

    SPINNER_TYPES = {
        "idle"          : "arc",
        "starting"      : "circle",
        "downloading"   : "dots",
        "paused"        : "toggle6",
        "failure"       : "star2",
        "success"       : "toggle9",
    }

    def __init__(
        self,
        custom_spinners: Optional[Dict[str, str]] = None,
        spinner_style: str = "progress.spinner",
        rotation_speed: float = 1.0,
    ):
        custom_spinners = custom_spinners or {}
        configured_spinners = {
            state: custom_spinners.get(state, default_spinner)
            for state, default_spinner in self.SPINNER_TYPES.items()
        }
        self.spinner_objects = {
            state: Spinner(
                spinner_type,
                style=spinner_style,
                speed=rotation_speed
            )
            for state, spinner_type in configured_spinners.items()
        }
        super().__init__()

    def render(self, task: Task):
        task_time = task.get_time()
        task_state = task.fields.get("state", "starting")
        spinner = self.spinner_objects.get(task_state, self.spinner_objects["starting"])
        return spinner.render(task_time)


class PercentageColumn(ProgressColumn):
    """
    A column to display progress percentage.
    """

    def __init__(
        self,
        text_format: str = "[progress.percentage]{task.percentage:>3.1f}%",
        style: str = "none",
        justify: str = "left",
    ):
        self.text_objects = TextColumn(
            text_format,
            style=style,
            justify=justify,
        )
        super().__init__()

    def render(self, task: Task):
        return self.text_objects.render(task)


class DescriptionColumn(ProgressColumn):
    """
    A column to display task description.
    """

    def __init__(
        self,
        text_format: str = "[yellow]{task.description}[/] | [blue]{task.fields[filename]}[/]",
        style: str = "none",
        justify: str = "left",
    ):
        self.text_objects = TextColumn(
            text_format,
            style=style,
            justify=justify,
        )
        super().__init__()

    def render(self, task: Task):
        return self.text_objects.render(task)


class Column:
    """
    Default columns for progress display
    """
    def __init__(self):
        self.columns = {
            "spinner"           : SpinnerColumn(),
            "description"       : DescriptionColumn(),
            "progress_bar"      : BarColumn(),
            "percentage"        : PercentageColumn(),
            "divider"           : "|"
        }

    def default(self):
        return self.columns.copy()

    def download(self):
        """
        Columns configured for download display.
        """
        self.columns["file_size"] = DownloadColumn()
        self.columns["transfer_speed"] = TransferSpeedColumn()
        self.columns["estimated_time"] = "•"
        self.columns["time_remaining"] = TimeRemainingColumn()
        return self.columns.copy()

    def generate(self):
        """
        Columns configured for spinner display.
        """
        self.columns.pop("progress_bar")
        self.columns.pop("percentage")
        self.columns.pop("divider")
        return self.columns.copy()

    def edit(self):
        """
        Columns configured for edit display.
        """
        self.columns["time_remaining"] = TimeRemainingColumn()
        return self.columns.copy()

    def wait(self):
        """
        Columns configured for wait display.
        """
        self.columns.pop("percentage")
        self.columns.pop("divider")
        self.columns["divider"] = "•"
        self.columns["time_elapsed"] = TimeElapsedColumn()
        return self.columns.copy()


class Progress:
    """
    Progress display manager
    """

    def __init__(
        self,
        spinner_column: SpinnerColumn = None,
        specific_columns: Optional[Dict[str, ProgressColumn]] = None,
        bar_size: Optional[int] = None,
        full_width: bool = False,
    ):
        self.columns = specific_columns or Column().default()
        self.progress_bar = self.columns.get('progress_bar')

        if spinner_column:
            self.columns = {"spinner": spinner_column, **self.columns}
        if isinstance(self.progress_bar, BarColumn):
            self.progress_bar.bar_width = bar_size or 55

        self.progress_display = RichProgress(
            *self.columns.values(),
            transient=False,
            redirect_stdout=True,
            redirect_stderr=True,
            expand=full_width,
        )
        self.progress_lock = Lock()
        self.running_tasks = set()

    async def add_task(
        self,
        description: str,
        start: bool = True,
        total_units: Optional[float] = None,
        units_done: int = 0,
        is_visible: bool = True,
        file_name: str = "",
        current_state: str = "starting",
    ) -> TaskID:
        async with self.progress_lock:
            task_id = self.progress_display.add_task(
                description=description,
                start=start,
                total=total_units,
                completed=units_done,
                visible=is_visible,
                filename=file_name,
                state=current_state,
            )
            self.running_tasks.add(task_id)
        return task_id

    async def update_task(
        self,
        task_id: TaskID,
        new_description: Optional[str] = None,
        new_total: Optional[float] = None,
        new_completed: Optional[float] = None,
        progress_increment: Optional[float] = None,
        still_visible: bool = True,
        force_refresh: bool = False,
        file_name=None,
        new_state: Optional[str] = None,
    ) -> None:
        async with self.progress_lock:
            update_params = [
                ("advance", progress_increment),
                ("description", new_description),
                ("state", new_state),
                ("filename", file_name),
            ]
            filtered_params = {key: value for key, value in update_params if value is not None}

            self.progress_display.update(
                task_id,
                total=new_total,
                completed=new_completed,
                visible=still_visible,
                refresh=force_refresh,
                **filtered_params,
            )
            # Check if the specified task is finished and still tracked as running
            is_task_finished = self.progress_display.tasks[task_id].finished

            if is_task_finished:
                if task_id in self.running_tasks:
                    # Remove the task from the running tasks list
                    self.running_tasks.remove(task_id)

    def start(self):
        self.progress_display.start()

    def start_task(self, task_id):
        self.progress_display.start_task(task_id)

    def end(self):
        self.progress_display.stop()

    def end_task(self, task_id):
        self.progress_display.stop_task(task_id)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()

    @property
    def active_tasks(self):
        return self.progress_display.tasks


class Console(metaclass=Singleton):
    """
    Main console management class
    """

    def __init__(self):
        pass

    def progress_bar(
        self,
        column_config: Optional[Dict[str, ProgressColumn]] = None,
    ) -> Progress:
        """
        Create a progress bar
        """
        self._progress = Progress(specific_columns=column_config)
        return self._progress

# Create a global instance of the console
# console = Console()