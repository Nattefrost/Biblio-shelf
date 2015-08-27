#!/bin/bash
if which xdg-open > /dev/null
then
	xdg-open http://192.168.1.21/cgi-bin/livres
elif which gnome-open > /dev/null
then
	gnome-open http://192.168.1.21/cgi-bin/livres
fi
