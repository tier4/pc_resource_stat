#!/usr/bin/sh

mkdir -p data
mkdir -p data/net_dev
mkdir -p data/iostat
mkdir -p data/free
mkdir -p data/net_tcp
mkdir -p data/net_udp

mkdir -p data/ps
ps aux -T > data/ps/`date --iso-8601=seconds`.txt

while true
do
  sleep 1
  cat /proc/net/dev > data/net_dev/`date --iso-8601=seconds`.txt
  iostat > data/iostat/`date --iso-8601=seconds`.txt
  free > data/free/`date --iso-8601=seconds`.txt
  cat /proc/net/tcp > data/net_tcp/`date --iso-8601=seconds`.txt
  cat /proc/net/udp > data/net_udp/`date --iso-8601=seconds`.txt
done
