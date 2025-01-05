import numpy as np
import matplotlib.pyplot as plt

def plot_waveform(audio_data, sample_rate,output_filepath):
    try:
        duration = len(audio_data) / sample_rate
        time = np.linspace(0., duration, len(audio_data))
        plt.figure(figsize=(10, 4))
        plt.plot(time, audio_data)
        plt.title("Waveform")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.tight_layout()
        plt.savefig(output_filepath)

    except Exception as e:
        raise ValueError(f"波形プロット時にエラーが発生しました: {e}")
