#!/bin/bash

echo 'Updating maps attributes ...'

cd ./external_data
python adding_attributes_to_maps.py

echo 'Done'