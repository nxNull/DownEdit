from moviepy import (
    afx,
    vfx,
    VideoFileClip,
    AudioFileClip
)
from ...edit.base import Editor


class VideoEditor(Editor):
    def __init__(self, input_path = "", output_path = ""):
        super().__init__(input_path, output_path)
        self.clip = VideoFileClip(self.input_path)

    def flip(self):
        """
        Flips the video horizontally.
        """
        self.clip = self.clip.with_effects([vfx.MirrorX()])
        return self

    def speed(self, factor = 1.0):
        """
        Changes the playback speed of the video based on the provided speed factor.

        Args:
            factor (float, optional): The speed factor to apply. Values:

                - Less than 1.0: Slows down the video (e.g., 0.5 for half speed).
                - Equal to 1.0: Plays the video at normal speed.
                - Greater than 1.0: Speeds up the video (e.g., 2.0 for double speed).

            Defaults to 1.0 (normal speed).
        """
        self.clip = self.clip.with_effects([vfx.MultiplySpeed(factor)])
        return self

    def add_music(self, music_path):
        """
        Adds background music to the video

        Args:
            music_path (str): The path to the audio file to be used as background music.
        """
        audio_clip = AudioFileClip(music_path)
        final_duration = self.clip.duration
        new_audio_clip = audio_clip.with_effects([afx.AudioLoop(duration=final_duration)])
        self.clip = self.clip.with_audio(new_audio_clip)
        return self

    def loop(self, amount=1):
        """
        Loops the video a specified number of times.

        Args:
            amount (int, optional): The number of times to loop the video. Defaults to 1.
        """
        self.clip = self.clip = self.clip.with_effects([vfx.Loop(n=amount)])
        return self

    def adjust_color(self, brightness=1, contrast=1, saturation=1):
        """
        Adjusts the color properties (brightness, contrast, saturation) of the video.

        Args:
            brightness (float, optional): The brightness factor to apply. Defaults to 1.0.
            contrast (float, optional): The contrast factor to apply. Defaults to 1.0.
            saturation (float, optional): The saturation factor to apply. Defaults to 1.0.
        """

        return self

    async def render(
        self,
        threads: int = 1,
        preset: str = "medium"
    ):
        """
        Writes the modified video to the specified output path.

        Args:
            `threads (int, optional)`: The number of threads to use for video encoding. This can improve performance on multi-core systems.
                - Defaults to 1 (single thread).
                - Choose a value based on your system's capabilities and workload.

            `preset (str, optional)`: The encoding preset to use, affecting speed and quality. Options include:

                - ultrafast (fastest, lowest quality)
                - superfast (very fast, low quality)
                - veryfast (fast, lower quality)
                - faster (balanced speed and quality)
                - fast (slightly slower, better quality)
                - medium (moderate speed, good quality)
                - slow (slower, highest quality)

                Defaults to 'medium' for a balance of speed and quality.
                - Consider your target audience and desired video file size when choosing a preset.
        """
        try:
            self.clip.write_videofile(
                self.output_path,
                logger=None,
                codec='libx264',
                audio_codec="aac",
                threads=threads,
                preset=preset
            )
        finally:
            self.clip.close()