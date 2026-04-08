import numpy as np
import scipy.io.wavfile as wav
import argparse

def comb_filter(x, delay_samples, gain):
    """
    Implements a feedback comb filter.
    y[n] = x[n] + gain * y[n - delay]
    """
    y = np.zeros(len(x))
    for i in range(len(x)):
        if i < delay_samples:
            y[i] = x[i]
        else:
            y[i] = x[i] + gain * y[i - delay_samples]
    return y

def allpass_filter(x, delay_samples, gain):
    """
    Implements an all-pass filter (Schroeder's design).
    y[n] = -gain * x[n] + x[n - delay] + gain * y[n - delay]
    """
    y = np.zeros(len(x))
    for i in range(len(x)):
        if i < delay_samples:
            y[i] = -gain * x[i]
        else:
            y[i] = -gain * x[i] + x[i - delay_samples] + gain * y[i - delay_samples]
    return y

def schroeder_reverberator(audio_in, sample_rate, mix=0.5):
    """
    Main Schroeder Reverb topology: 4 parallel comb filters into 2 series all-pass filters.
    Delay times are chosen as mutually prime numbers to avoid resonance overlap.
    """
    # 1. Delay times in seconds (standard Schroeder tuning)
    comb_delays_sec = [0.0297, 0.0371, 0.0411, 0.0437] 
    allpass_delays_sec = [0.0050, 0.0017]
    
    # 2. Convert to samples
    C_delays = [int(d * sample_rate) for d in comb_delays_sec]
    A_delays = [int(d * sample_rate) for d in allpass_delays_sec]
    
    # 3. Filter Gains
    C_gains = [0.75, 0.73, 0.71, 0.69]  # Determines RT60 (Reverb Time)
    A_gains = [0.7, 0.7]

    # 4. Parallel Comb Filters
    c1 = comb_filter(audio_in, C_delays[0], C_gains[0])
    c2 = comb_filter(audio_in, C_delays[1], C_gains[1])
    c3 = comb_filter(audio_in, C_delays[2], C_gains[2])
    c4 = comb_filter(audio_in, C_delays[3], C_gains[3])
    
    # Sum parallel filters
    comb_sum = c1 + c2 + c3 + c4

    # 5. Series All-Pass Filters
    a1 = allpass_filter(comb_sum, A_delays[0], A_gains[0])
    y_wet = allpass_filter(a1, A_delays[1], A_gains[1])

    # 6. Wet/Dry Mix
    # Normalize wet signal to prevent clipping
    if np.max(np.abs(y_wet)) > 0:
        y_wet = y_wet / np.max(np.abs(y_wet)) 
    
    y_out = (1 - mix) * audio_in + mix * y_wet
    return y_out

if __name__ == "__main__":
    # Example usage for testing
    sample_rate, audio_data = wav.read("input_dry.wav")
    
    # Convert to mono float if stereo/int
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Apply Reverb
    processed_audio = schroeder_reverberator(audio_data, sample_rate, mix=0.4)
    
    # Save output
    wav.write("output_reverb.wav", sample_rate, np.int16(processed_audio * 32767))
    print("Reverb applied and saved to output_reverb.wav")
