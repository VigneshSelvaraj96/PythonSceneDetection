import os
import subprocess

# video_file = "./data/The_Long_Dark_rgb/InputVideo.rgb"
# audio_file = "./data/The_Long_Dark_rgb/InputAudio.wav"
dirname = os.path.dirname(__file__)
video_file = os.path.join(dirname, './Data/InputVideo.rgb')
audio_file = os.path.join(dirname, './Data/InputAudio.wav')
output_file = os.path.join(dirname, './Data/InputVideo.mp4')

# Set the video and audio input options
video_input_options = "-f rawvideo -pix_fmt rgb24 -s:v 480x270 -r 30"
audio_input_options = "-i"

# Set the output options
output_options = "-c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k"

# Build the ffmpeg command
ffmpeg_cmd = f"ffmpeg {video_input_options} -i {video_file} {audio_input_options} {audio_file} -map 0:v -map 1:a {output_options} {output_file}"

# Execute the ffmpeg command
subprocess.call(ffmpeg_cmd, shell=True)