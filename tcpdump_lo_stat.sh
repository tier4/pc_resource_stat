#!/usr/bin/sh

mkdir -p data2
ps aux -T > data2/ps.txt
lsof > data2/lsof.txt
sudo tcpdump -n -i lo > data2/tcpdump.txt