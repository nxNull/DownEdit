from ._operation import (
    AIImgGenAPI,
    AIImgGenOperation,
)

class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> AIImgGenOperation:
        """
        Creates a image generation operation based on the operation name and parameters.

        Args:
            operation_name (str):

        Returns:
            AIImgGenOperation: The image generation operation instance.
        """
        operations = {
            "ai_img_gen": AIImgGenAPI
        }
        operation_class = operations.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)