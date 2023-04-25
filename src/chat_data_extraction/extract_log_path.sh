#!/bin/bash

project_dir=$(pwd)'/logs_data/log_paths.txt'

cd C:\Users
cd $(find -path './*/AppData/Roaming/.minecraft' ! -path './Default/*' -print -quit )
cd logs

realpath $(find -name '*.log.gz')
realpath $(find -name '*.log.gz') > $project_dir

python compact_logs.py