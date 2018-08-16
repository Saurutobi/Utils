#!/bin/sh
echo Launching WinMergeU.exe: $1 $2
"$PROGRAMFILES (x86)\WinMerge\WinMergeU.exe" -e -ub -dl "Base --> $1" -dr "Mine --> $2" "$1" "$2"