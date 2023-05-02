import numpy as np
import librosa
from scenedetect import SceneManager, open_video, ContentDetector
import scenedetect
import datetime
import json

import os

dirname = os.path.dirname(__file__)

# Define the path to the audio file
audio_path = os.path.join(dirname, './Data/InputAudio.wav')
video_path = os.path.join(dirname, './Data/InputVideo.mp4')


# Define a dict to hold all our data values. I am using start times here as the index

dict_of_start_times = {}

scene_threshold = 50
# threshold (float) – Threshold the average change in pixel intensity must exceed to trigger a cut.

shot_threshold = 35
# threshold (float) – Threshold the average change in pixel intensity must exceed to trigger a cut.

min_scene_length = 60
# Once a cut is detected, this many frames must pass before a new one can be added to the scene list.

min_shot_length = 50


# Once a cut is detected, this many frames must pass before a new shot can be added to the shot list.

def main():
    def find_scenes(video_path):
        video = open_video(video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(
            ContentDetector(threshold=scene_threshold, min_scene_len=min_scene_length))
        # Detect all scenes in video from current position to end.
        scene_manager.detect_scenes(video)
        # `get_scene_list` returns a list of start/end timecode pairs
        # for each scene that was found.
        return scene_manager.get_scene_list()

    print('Detecting Scenes...')
    scenes = find_scenes(video_path)
    detector = scenedetect.detectors.ContentDetector(threshold=shot_threshold, min_scene_len=min_shot_length)

    for scene in scenes:
        scene_start = scene[0].get_timecode()
        scene_end = scene[1].get_timecode()
        # Now we use scene detect again on the original video, but this time we use the scene list to use the start and stop times to create shots
        # create ContentDetector object with a threshold
        print('Detecting Shot...')
        shots = scenedetect.detect(video_path, detector=detector, start_time=scene_start,
                                   end_time=scene[1].get_timecode())
        # create a new list with shots that have different start and stop timecode
        filtered_shots = [shot for shot in shots if shot[0].get_timecode() != shot[1].get_timecode()]
        dict_of_start_times[scene_start] = {}
        for shot in filtered_shots:
            print('Detecting Subshot...')
            shot_start = shot[0].get_timecode()
            shot_end = shot[1].get_timecode()
            start_delta = datetime.datetime.strptime(shot_start, "%H:%M:%S.%f") - datetime.datetime.strptime(
                "00:00:00.000", "%H:%M:%S.%f")
            end_delta = datetime.datetime.strptime(shot_end, "%H:%M:%S.%f") - datetime.datetime.strptime("00:00:00.000",
                                                                                                         "%H:%M:%S.%f")
            duration = (end_delta - start_delta).total_seconds()
            # Load the audio waveform between the start and stop times
            waveform, sample_rate = librosa.load(audio_path, sr=None, offset=start_delta.total_seconds(),
                                                 duration=duration)
            # Calculate the absolute difference between successive samples
            diff = np.abs(np.diff(waveform))

            # Define the delta threshold above which a shot change is detected. In our case, i decided to use RMS since we don't know the
            # avg change of waves without manual inspection. Professor will give us a random one anyway
            delta_threshold = np.sqrt(np.mean(np.square(waveform))) * 2.5

            # Initialize the start and stop times list
            start_stop_times = []

            # Find the start and stop times for each scene change
            # im setting a 1 second minimum for audio classification here so it is not changing rapidly
            start = 0
            for i in range(1, len(diff)):
                if diff[i] > delta_threshold:
                    # Use the sample index where the threshold is exceeded as the stop time
                    stop = i
                    if (stop - start) / sample_rate > 1:  # Minimum duration of 1 second
                        start_stop_times.append((start / sample_rate + start_delta.total_seconds(),
                                                 stop / sample_rate + start_delta.total_seconds()))
                        start = i

            # Add the final scene if necessary
            if start < len(waveform):
                stop = len(waveform)
                if (stop - start) / sample_rate > 1:  # Minimum duration of 1 second
                    start_stop_times.append((start / sample_rate + start_delta.total_seconds(),
                                             stop / sample_rate + start_delta.total_seconds()))

            for tuple in start_stop_times:
                list_of_subshots = [t[0] for t in start_stop_times]
                dict_of_start_times[scene_start][shot_start] = {}
                dict_of_start_times[scene_start][shot_start] = list_of_subshots

    file_name = os.path.join(dirname, './Data/dict_of_start_times.json')
    with open(file_name, 'w') as fp:
        json.dump(dict_of_start_times, fp, indent=4)


if __name__ == "__main__":
    main()
