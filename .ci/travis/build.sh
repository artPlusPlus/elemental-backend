#!/usr/bin/env bash

conda build --channel artplusplus ./.conda.recipe
conda install --channel artplusplus --use-local elemental-backend
py.test

source deactivate
python ./.ci/move_conda_package.py ./.conda.recipe
