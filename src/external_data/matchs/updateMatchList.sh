#!/bin/bash


cd ./external_data/matchs

#Update match list status
#/code/

new_data_file='new_data.csv'
origin_data_file='data.csv'
echo "fuck off"


#Stardization of data
echo 'Standardization of matchs data ...'
python standardization_data.py --origin $origin_data_file --new $new_data_file

#Adding match data to database
echo 'Adding match to database ...'
python match_to_database.py --path $new_data_file


