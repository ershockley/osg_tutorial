#!/usr/bin/env bash

. /opt/XENONnT/setup.sh

export RUCIO_ACCOUNT=xenon-analysis
export XENON_CONFIG=$PWD/.xenon_config
rucio whoami

python -c "import strax; print(strax.__file__)"

python -c "from utilix import db"
q