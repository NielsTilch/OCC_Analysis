#!/bin/bash

echo "Welcome to the transfer menu"

echo "1- Specific transfer of a map"
echo "2- Batch of top maps transfer"
echo "3- Reset map file"

read -p "Choice of transfer : " choice

if [ $choice = '2' ];then
  cd ./top_map
  bash top_map_transfer.sh
fi

if [ $choice = '1' ];then
  cd ./specific_map
  bash specific_map_transfer.sh
fi

if [ $choice = '3' ];then
  cd C:\Users
  mc_file=$(find -path './*/AppData/Roaming/.minecraft' ! -path './Default/*' -print -quit )
  mc_file="${mc_file:1}"
  mc_path=$(pwd)$mc_file
  cd $mc_path
  rm -r saves
  mkdir saves
fi