#!/usr/bin/sh

DIR_NAME=$1

mkdir -p $DIR_NAME
ps aux -T >$DIR_NAME/ps.txt
lsof >$DIR_NAME/lsof.txt
sudo tcpdump -n -i lo >$DIR_NAME/tcpdump.txt
