from ._operation import (
    VideoOperation,
    Flip,
    Speed,
    AddMusic,
    Loop,
    AdjustColor
)


OPERATIONS = {
    "flip"        : Flip,
    "speed"       : Speed,
    "add_music"   : AddMusic,
    "loop"        : Loop,
    "adjust_color": AdjustColor,
}


class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> VideoOperation:
        """
        Creates a video editing operation based on the operation name and parameters.

        Args:
            operation_name (str):
                - `flip`: Flip a video.
                - `speed`: Change the speed of a video.
                - `add_music`: Add music to a video.
                - `loop`: Loop a video.
                - `adjust_color`: Adjust the color of a video.

        Returns:
            VideoOperation: A video operation object.
        """
        operation_class = OPERATIONS.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)