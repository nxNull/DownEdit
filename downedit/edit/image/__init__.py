from ._operation import (
    ImageOperation,
    Flip,
    Crop,
    Enhance,
    Rotate,
    Resize,
    GrayScale,
    Sharpen,
    Blur
)


OPERATIONS = {
    "flip"      : Flip,
    "crop"      : Crop,
    "enhance"   : Enhance,
    "rotate"    : Rotate,
    "resize"    : Resize,
    "grayscale" : GrayScale,
    "sharpen"   : Sharpen,
    "blur"      : Blur
}


class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> ImageOperation:
        """
        Creates a image editing operation based on the operation name and parameters.

        Args:
            operation_name (str):
                - `flip`: Flip an image.
                - `crop`: Crop an image.
                - `enhance`: Enhance an image.
                - `rotate`: Rotate an image.
                - `resize`: Resize an image.
                - `grayscale`: Convert an image to grayscale.
                - `sharpen`: Sharpen an image.
                - `blur`: Blur an image.

        Returns:
            ImageOperation: An image operation object.
        """
        operation_class = OPERATIONS.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)