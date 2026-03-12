#!/bin/bash

# Activate the charts environment
conda init
conda activate charts

# Run the chart generator app
python main.py

# Optional: deactivate the environment when done
conda deactivate
