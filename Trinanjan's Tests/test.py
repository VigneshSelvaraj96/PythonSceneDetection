import scenedetect
from scenedetect import detect, ContentDetector, split_video_ffmpeg
scene_list = detect('output-Scene-008.mp4', show_progress=True, detector=scenedetect.AdaptiveDetector())
# split_video_ffmpeg('output.mp4', scene_list, show_progress=True)
for i, scene in enumerate(scene_list):
    print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
        i+1,
        scene[0].get_timecode(), scene[0].get_frames(),
        scene[1].get_timecode(), scene[1].get_frames(),))


