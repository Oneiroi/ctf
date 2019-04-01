#!/bin/bash

zip2jtr=`which zip2john`


usage() {
    echo "Useage: $0 /path/to/file.zip"
}

[[ -z "$zip2jtr" ]] && echo "zip2john could not be found, have you installed john the ripper ? exiting ..." && exit 1;

[[ -z "$1" ]] && usage && exit 1 

$zip2jtr $1 | cut -d ':' -f 2 2>/dev/null
