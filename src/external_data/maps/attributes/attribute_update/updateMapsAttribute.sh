#!/bin/bash

echo 'Updating maps attributes ...'

#Going to source file
cd ./../../../..

#Running adding attribute program
python -m external_data.maps.attributes.attribute_update.adding_attributes_to_maps

echo 'Done'