#!/bin/bash

python3 -m venv .env
source .env/bin/activate

python -m pip install -U numpy
python -m pip install -U matplotlib
  # -U indicates that if the package already exists it should be upgraded.