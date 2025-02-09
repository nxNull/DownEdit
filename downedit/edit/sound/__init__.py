from ._operation import (
    SoundOperation,
    Volume,
    FadeIn,
    FadeOut
)


OPERATIONS = {
    "volume"     : Volume,
    "fade in"    : FadeIn,
    "fade out"   : FadeOut
}


class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> SoundOperation:
        """
        Creates a video editing operation based on the operation name and parameters.

        Args:
            operation_name (str):
                - `Volume`: Change the volume of a sound.
                - `Fade In`: Fade in a sound.
                - `Fade Out`: Fade out a sound.

        Returns:
            SoundOperation: A sound operation object.
        """
        operation_class = OPERATIONS.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)