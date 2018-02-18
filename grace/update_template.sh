#! /bin/sh
./strip $1 > temp
./merge template.htmlt temp $3 > temp1
cp temp1 $1
