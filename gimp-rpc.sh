#!/bin/bash
GIMPNEW=$(wmctrl -l | grep -o "$HOSTNAME.*" | sed "s/$HOSTNAME //g" | grep -F 'GNU Image Manipulation Program')
GIMPOPEN=$(wmctrl -l | grep -o "$HOSTNAME.*" | sed "s/$HOSTNAME //g" | grep -F '– GIMP')
if [[ ! -z $GIMPNEW ]]; then
	if [[ $1 = "line2" ]]; then
		. /etc/os-release
		echo -n 'Distro: '$PRETTY_NAME
	elif [[ $1 = "line1" ]]; then
		echo -n 'Idle'
	else
		:
	fi
elif [[ ! -z $GIMPOPEN ]]; then
	IMAGENAME=$(echo -n $GIMPOPEN | grep -o -P '(?<=\[).*(?=\])')
	IMAGEDIMENSION=$(echo -n $GIMPOPEN | sed 's~ – GIMP~~' | awk '{print $NF}')
	if [[ ! -z $IMAGENAME ]]; then
		if [[ $1 = "line2" ]]; then
			echo -n $IMAGENAME' ['$IMAGEDIMENSION']'
		elif [[ $1 = "line1" ]]; then
			echo -n 'Editing'
		else
			:
		fi
	else
		if [[ $1 = "line2" ]]; then
			echo -n $(wmctrl -l | grep -o "$HOSTNAME.*" | sed "s/$HOSTNAME //g" | grep -F '– GIMP' | sed -r "s=(\().*==")
		elif [[ $1 = "line1" ]]; then 
			echo -n 'Editing'
		else
			:
		fi
	fi
else
	echo "ERROR_BREAK"
fi

if [[ $1 = "version" ]]; then
	echo -n 'Version: '$(/usr/bin/gimp -v | grep -F 'GNU Image Manipulation Program' | sed 's~GNU Image Manipulation Program version ~~g')
fi
