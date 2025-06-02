from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip, ColorClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
# from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx import all as vfx
from moviepy.audio.fx import all as afx
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip, CompositeAudioClip
from moviepy.video.tools.drawing import color_gradient

# Export names so you can do: import moviepy.editor as mp
__all__ = [
    "VideoFileClip",
    "TextClip",
    "ColorClip",
    "ImageClip",
    "CompositeVideoClip",
    "concatenate_videoclips",
    "vfx",
    "afx",
    "AudioFileClip",
    "AudioClip",
    "CompositeAudioClip",
    "color_gradient"
]
