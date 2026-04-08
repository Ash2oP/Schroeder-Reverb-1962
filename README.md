# Natural-Sounding Artificial Reverberation (Schroeder, 1962)

This repository contains a Python implementation of the digital reverberator proposed by Manfred R. Schroeder in his 1962 paper, "Natural-Sounding Artificial Reverberation."

## Overview
The algorithm simulates acoustic room reflections using a specific topology of digital delay lines:
1. **Four Parallel Comb Filters:** To simulate the exponential decay of sound (RT60) and generate early reflections.
2. **Two Series All-Pass Filters:** To drastically increase the echo density without coloring the frequency response of the audio.

## Installation and Usage
Dependencies: `numpy`, `scipy`

1. Clone the repository: `git clone [your-github-link]`
2. Place a dry `.wav` file in the directory.
3. Run the script: `python src/schroeder_reverb.py`

## Citation
> M. R. Schroeder, "Natural-Sounding Artificial Reverberation," Journal of the Audio Engineering Society, vol. 10, no. 3, pp. 219-223, July 1962.
