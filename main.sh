#!/usr/bin/env bash
# pipeline for Jump Entropy project
echo pipeline init
while true;do echo -n ':( ';sleep 1;done &
cd src
python ngram_vis.py
python scopus_vis.py
cd ..
kill $!; trap 'kill $!' SIGTERM
echo
echo ':)'
