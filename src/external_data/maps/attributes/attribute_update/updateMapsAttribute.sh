#!/bin/bash

echo 'Updating maps attributes ...'

cd ./../../../..

python -m external_data.maps.attributes.attribute_update.adding_attributes_to_maps

echo 'Done'