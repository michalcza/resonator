import numpy as np
import pyaudio

# Parameters for audio playback
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
DURATION = 5  # Duration of the audio in seconds

# Function to generate a sine wave with a frequency sweep
def generate_sweep(start_freq, end_freq, duration, rate):
    t = np.linspace(0, duration, int(duration * rate), endpoint=False)
    frequencies = np.linspace(start_freq, end_freq, len(t))
    sweep = np.sin(2 * np.pi * frequencies * t)
    return sweep

# Define the start and end frequencies for the sweep
start_freq = 400  # Hz
end_freq = 800  # Hz

# Generate the frequency sweep waveform
sweep_waveform = generate_sweep(start_freq, end_freq, DURATION, RATE)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream to play the audio
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

# Play the frequency sweep
stream.write(sweep_waveform.astype(np.float32).tobytes())

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
audio.terminate()
