import numpy as np
import pyaudio
import threading
import time

# Parameters for audio playback
PLAYBACK_FORMAT = pyaudio.paFloat32
PLAYBACK_CHANNELS = 1
PLAYBACK_RATE = 44100
PLAYBACK_DURATION = 5  # Duration of the audio in seconds

# Parameters for audio recording
RECORD_FORMAT = pyaudio.paFloat32
RECORD_CHANNELS = 1
RECORD_RATE = 44100
RECORD_DURATION = PLAYBACK_DURATION  # Duration of the recording in seconds

# Function to generate a sine wave with multiple frequencies
def generate_wave(frequencies, duration, rate):
    t = np.linspace(0, duration, int(duration * rate), endpoint=False)
    wave = np.sum([np.sin(2 * np.pi * f * t) for f in frequencies], axis=0)
    return wave

# Function to record audio
def record_audio(stream, frames, chunk_size):
    while True:
        data = stream.read(chunk_size)
        frames.append(data)

# Function to calculate the FFT and find the peak frequency
def find_resonant_frequency(signal, rate):
    # Perform FFT (Fast Fourier Transform) on the signal
    fft_result = np.fft.fft(signal)

    # Get the magnitudes of the FFT bins
    magnitude = np.abs(fft_result)

    # Find the index of the maximum magnitude
    max_index = np.argmax(magnitude)

    # Calculate the corresponding frequency
    freqs = np.fft.fftfreq(len(signal), 1/rate)
    resonant_freq = freqs[max_index]

    return resonant_freq

# Initialize PyAudio for playback
audio_player = pyaudio.PyAudio()

# Initialize PyAudio for recording
audio_recorder = pyaudio.PyAudio()

# Open a stream for playback
play_stream = audio_player.open(format=PLAYBACK_FORMAT,
                                channels=PLAYBACK_CHANNELS,
                                rate=PLAYBACK_RATE,
                                output=True)

# Open a stream for recording
record_stream = audio_recorder.open(format=RECORD_FORMAT,
                                    channels=RECORD_CHANNELS,
                                    rate=RECORD_RATE,
                                    input=True,
                                    frames_per_buffer=1024)  # Use a smaller chunk size

# Define the frequencies you want to generate
frequencies = [440, 880, 1320]  # Example frequencies (440 Hz, 880 Hz, 1320 Hz)

# Generate the waveform
waveform = generate_wave(frequencies, PLAYBACK_DURATION, PLAYBACK_RATE)

# Create a list to store recorded frames
record_frames = []

# Start recording thread
record_thread = threading.Thread(target=record_audio, args=(record_stream, record_frames, 1024))
record_thread.start()

# Play audio and simultaneously record
for _ in range(int(RECORD_RATE * RECORD_DURATION / 1024)):
    play_stream.write(waveform.astype(np.float32).tobytes())

# Stop recording thread
record_thread.join()

# Close the streams and terminate PyAudio
play_stream.stop_stream()
play_stream.close()
record_stream.stop_stream()
record_stream.close()
audio_player.terminate()
audio_recorder.terminate()

# Convert recorded frames to numpy array
recorded_data = np.frombuffer(b''.join(record_frames), dtype=np.float32)

# Calculate the resonant frequency from recorded audio data
resonant_frequency = find_resonant_frequency(recorded_data, RECORD_RATE)
print("Resonant Frequency:", resonant_frequency, "Hz")
