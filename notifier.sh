#!/bin/bash

# This script is require to maintain if the script has to run now or not using monit

if [[ $(date +%u) -lt 6 ]] ; then
  hours=$(date +%H)
  if [[ $((10#$hours)) -ge 8 ]] && [[ $((10#$hours)) -le 16 ]]; then
    python3 app/crawler/notifier.py
  else
    echo "no no"
  fi
fi
