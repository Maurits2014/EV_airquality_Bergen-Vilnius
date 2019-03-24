#!/bin/bash
# bash 4.4.023-1
# coreutils 8.30-1


# check if parameter is supplied
if [ -z "$1" ]
then
   echo "Pass file using command line argument" >&2
   exit -1
fi

(head -n 1 "$1" && tail -n +2 "$1" | sort)
