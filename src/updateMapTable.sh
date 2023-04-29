#!/bin/bash

cd ./external_data/maps

if ! test -f "./CommunityMaps" ;
then
echo "fuck off"

#Update projects
cd ./CommunityMaps
git pull
cd ./../PublicMaps
git pull
cd ./../../..


else

#Git clone repository
git clone https://github.com/OvercastCommunity/PublicMaps.git
git clone https://github.com/OvercastCommunity/CommunityMaps.git

fi

pwd
find -name 'map.xml' > ./external_data/maps/list_path_xmls.txt

echo "Starting mapping to SQL ..."
python -m external_data.maps.map_mapping

echo "Done"