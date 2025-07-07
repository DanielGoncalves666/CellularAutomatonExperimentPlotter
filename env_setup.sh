#!/bin/bash

python3 -m venv .env
source .env/bin/activate

python3 -m pip install -U numpy
python3 -m pip install -U matplotlib
python3 -m pip install -U PyQt6
  # -U indicates that if the package already exists it should be upgraded.
