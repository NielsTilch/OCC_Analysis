#!/bin/bash

cd ./..
file=$(pwd)'/file.txt'

#Going to source file
cd ./../../../..
source=$(pwd)
echo $source

#Running map transfer script
python -m external_data.maps.attributes.map_transfer.specific_map.map_transfer
echo 'Getting top map done'

cd C:\Users

#Searching mc file
mc_file=$(find -path './*/AppData/Roaming/.minecraft' ! -path './Default/*' -print -quit )
mc_file="${mc_file:1}"
mc_path=$(pwd)$mc_file

#Reseting saves fil in .minecraft
cd $mc_path
rm -r saves
mkdir saves

cd C:\Users

#Going through the list of map and copy past in .minecraft/saves
track=0
while read p; do

  #Copy paste map if odd
  if [ $((track%2)) == 0 ]; then
    map=$source$p
    map=${map::-1}
    cp -r $map $mc_path'/saves'

  #echo coords if even
  else
    echo $p
  fi
  ((track++))

done<$file


echo 'Done'
exit 0