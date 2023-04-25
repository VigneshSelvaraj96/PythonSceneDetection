from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np

# Load MP4 video file
video_path = './output-Scene-014.mp4'
audio = AudioSegment.from_file(video_path)

# Extract audio data as NumPy array
audio_data = np.array(audio.get_array_of_samples())

# Normalize audio data
audio_data = audio_data / 2**15  # Normalize to -1 to 1 range for 16-bit audio

# Calculate audio properties
sample_rate = audio.frame_rate
duration = audio.duration_seconds

# Generate time axis
time = np.linspace(0, duration, num=len(audio_data))

# Plot audio graph
plt.figure(figsize=(12, 6))
plt.plot(time, audio_data)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Audio Graph from MP4 Video')
plt.grid(True)
plt.show()






