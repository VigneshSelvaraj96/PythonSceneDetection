# Video Scene Detection

This is a Python Program that incorporates a Video Player that parses a WAV and RGB file input to construct an MP4 File with appropriate Time Stamps that users can navigate to for scene changes

## Libraries Used

- PySceneDetection
- Librosa
- PyQt5
- Numpy
- FFMPEG

## Execution Steps

The VideoPlayer directory contains the actual code scripts. All the input files must be kept inside the `Data` folder. There are three python scripts which should be executed in order as:

1. ` create_video_file.py` : It takes two inputs from the `Data` directory, `InputVideo.rgb` and `InputAudio.wav` and converts them to create `InputVideo.mp4` inside the same directory

2. `data_processing.py` : It reads the `InputVideo.mp4` and `InputAudio.wav` from the `Data` directory and perfoms analysis on both the video and audio data to detect the scenes, shots and subshots and stores them in `dict_of_start_times.json` as timestamp JSON format inside the same directory

3. `video_player.py` : It reads the `InputVideo.mp4` and `dict_of_start_times.json` from `Data` directory and runs an interactive video player instance where the scenes, shots and subshots are shown in a hierarchical view with user interaction feature.

<b><i>Note: All the file naming conventions must be exactly followed for successful execution of the scripts</i></b>

## Few Pointers and Summary

- We have used pyscenedetect library to detect the scenes and shots and designed a custom algorithm on audio waveform for the subshot detection. So the subshots are purely based on audio analysis

- We have used the Root Mean Square of the audio frequences to fix a threshold. This threshold is completely dynamic in nature.

- The threshold for the shot and scene changes are calculated in a trial and error basis. Whenever there is a major change in the entropy of two consecutive frames, a shot is detected and multiple shots are combined to form a meaningful scene

- We have used QtMultimedia features of PyQt5 for the video player. In some platforms, it might need an additional codec to show the video. An .exe file of K Light Codec is provided, which must be installed to resolve this issue.
