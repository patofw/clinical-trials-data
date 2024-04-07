#!/bin/bash

echo "CONDA-SYNC (0/1): Ensuring conda-lock is discoverable"
. ~/.bashrc

echo "CONDA SYNC (1/5): Installing clinical-trials-data-dev environment"
conda-lock install -n clinical-trials-data-dev --log-level ERROR

echo "CONDA SYNC (2/5): Activating clinical-trials-data-dev"
conda activate clinical-trials-data-dev

echo "CONDA SYNC (3/5): Installing clinical-trials-data as editable"
python -m pip install -e .

echo "CONDA SYNC (4/5): Installing pre-commit"
pre-commit install
pre-commit autoupdate

echo "CONDA SYNC (5/5): Running pre-commit"
pre-commit run -a
