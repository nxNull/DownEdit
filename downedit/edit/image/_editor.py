from PIL import (
    Image,
    ImageFilter,
    ImageEnhance
)

from downedit.edit.base import Editor


class ImageEditor(Editor):
    def __init__(self, input_path = "", output_path = ""):
        super().__init__(input_path, output_path)
        self._img = None

    def _get_properties(self):
        """Gets the properties of the image."""
        width, height = self._img.size
        min_side_length = min(width, height)

        left = (width - min_side_length) / 2
        upper = (height - min_side_length) / 2
        right = (width + min_side_length) / 2
        lower = (height + min_side_length) / 2

        return left, upper, right, lower

    def _load_image(self):
        """Loads the image from the input path."""
        if self.input_path is None:
            raise ValueError("Input path cannot be None")
        self._img = Image.open(self.input_path)
        return self

    def _save_image(self):
        """Saves the modified image to the output path."""
        if self.output_path is None:
            raise ValueError("Output path cannot be None")
        self._img.save(self.output_path)
        return self

    def transpose(self):
        """Transposes the image (flips horizontally)."""
        self._img = self._img.transpose(Image.FLIP_LEFT_RIGHT)
        return self

    def crop(self):
        """Crops the image to a square."""
        left, top, right, bottom = self._get_properties()
        self._img = self._img.crop((left, top, right, bottom))
        return self

    def enhance(self):
        """Enhances the image by increasing color and contrast."""
        self._img = ImageEnhance.Color(self._img).enhance(1.5)
        self._img = ImageEnhance.Contrast(self._img).enhance(1.5)
        return self

    def rotate(self, degrees):
        """Rotates the image by the specified degrees."""
        self._img = self._img.rotate(degrees)
        return self

    def resize(self, width, height):
        """Resizes the image to the specified width and height."""
        self._img = self._img.resize((width, height))
        return self

    def grayscale(self):
        """Converts the image to grayscale."""
        self._img = self._img.convert('L')
        return self

    def sharpen(self):
        """Sharpens the image."""
        self._img = ImageEnhance.Sharpness(self._img).enhance(1.5)
        return self

    def blur(self, radius = 2):
        """Blurs the image with the specified radius."""
        self._img = self._img.filter(ImageFilter.BLUR)
        return self
    
    def load(self):
        """Loads the image from the specified input path."""
        self._load_image()
        return self

    def save(self):
        """Saves the modified image to the specified output path."""
        self._save_image()
        return self
    
    def close(self):
        """Closes the image."""
        self._img.close()
        return self
    
    async def render(self):
        """Renders the image."""
        self.save().close()
        return self