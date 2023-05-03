#!/bin/bash

file=$(pwd)'/file.txt'

cd ./../../../../..
source=$(pwd)
echo $source
python -m external_data.maps.attributes.map_transfer.map_transfer
echo 'Getting top map done'

cd C:\Users

mc_file=$(find -path './*/AppData/Roaming/.minecraft' ! -path './Default/*' -print -quit )
mc_file="${mc_file:1}"
mc_path=$(pwd)$mc_file

cd $mc_path
rm -r saves
mkdir saves

cd C:\Users

track=0
while read p; do

  if [ $((track%2)) == 0 ]; then
    map=$source$p
    map=${map::-1}
    cp -r $map $mc_path'/saves'
  else
    echo $p
  fi
  ((track++))

done<$file


echo 'Done'
exit 0