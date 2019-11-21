#! /bin/bash

mkdir dataset/nonPorn
NONPORN=../dataset/nonPorn/ 
cd downloads
mv "beach clothes"/* $NONPORN
mv breastfeeding/*  $NONPORN
mv cat/* $NONPORN
mv games/* $NONPORN
mv "gym clothes"/* $NONPORN
mv swimming/* $NONPORN
mv wrestling/* $NONPORN

cd $NONPORN

echo "Número de arquivos é $(ls | wc -l)"

cd ../../