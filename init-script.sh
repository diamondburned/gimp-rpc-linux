#!/bin/bash

GIMP=$(ps -aux | grep $(whoami) | grep -v "grep" | grep -v "python" | grep "gimp")
DISCORD=$(ps -aux | grep $(whoami) | grep -v "grep" | grep -v "python" | grep "discord")
SCRIPTPID=$(ps -aux | grep $(whoami) | grep -v "grep" | grep "gimp-rpc.py" | awk '{print $2}')

if [[ -z $GIMP ]]; then
	echo -n ERROR_GIMP_NOT_FOUND' '
else
	:
fi

if [[ -z $DISCORD ]]; then
	echo -n ERROR_DISCORD_NOT_FOUND' '
else
	:
fi

NL='
'
case $SCRIPTPID in
  *"$NL"*) echo -n ERROR_SCRIPT_ALREADY_RUNNING' ' ;;
        *) : ;;
esac

if ping -i 500 -c 1 -W 1 discordapp.com >> /dev/null 2>&1; then
	: 
else
	echo -n ERROR_NO_CONNECTION' '
	exit 0
fi
