#!/bin/bash

SCRIPTPID=$(ps -aux | grep $(whoami) | grep -v "grep" | grep "gimp-rpc.py" | awk '{print $2}')

NL='
'
case $SCRIPTPID in
  *"$NL"*) echo -n ERROR_SCRIPT_ALREADY_RUNNING' ' ;;
        *) : ;;
esac

if ! type "wmctrl" &> /dev/null; then
	echo -n ERROR_WMCTRL_NOT_INSTALLED
	zenity --error --title="osu-wine" --width="350" --text="$(echo "Please install wmctrl\!\nFor references, see the README.md of the GitHub project.")" &> /dev/null
else
	:
fi