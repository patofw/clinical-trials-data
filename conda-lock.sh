#!/bin/bash

echo "CONDA-LOCK (0/1): Ensuring conda-lock is discoverable"
. ~/.bashrc

echo "CONDA-LOCK (1/1): Locking clinical-trials-data-dev environment with dependencies to 'conda-lock.yml'"
conda-lock lock -f environment.yml -f dev-environment.yml --lockfile conda-lock.yml --log-level ERROR
