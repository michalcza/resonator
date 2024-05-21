import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream to capture audio from the microphone
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Function to plot frequency spectrum
def plot_spectrum(y):
    plt.figure(figsize=(8, 4))
    plt.plot(y)
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.title('Time Domain Signal')
    plt.show()

def find_resonant_frequencies(signal):
    # Perform FFT (Fast Fourier Transform) on the signal
    fft_result = np.fft.fft(signal)

    # Get the magnitudes of the FFT bins
    magnitude = np.abs(fft_result)

    # Find the index of the maximum magnitude
    max_index = np.argmax(magnitude)

    # Calculate the corresponding frequency
    freqs = np.fft.fftfreq(len(signal), 1/RATE)
    resonant_freq = freqs[max_index]

    return resonant_freq

print("Listening... Press Ctrl+C to stop.")

try:
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        
        # Convert byte data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Plot time domain signal
        plot_spectrum(audio_data)

        # Find resonant frequency
        resonant_freq = find_resonant_frequencies(audio_data)
        print("Resonant Frequency:", resonant_freq, "Hz")
        
except KeyboardInterrupt:
    print("Stopped.")

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
audio.terminate()
