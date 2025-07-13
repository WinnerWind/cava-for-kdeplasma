#!/bin/bash
export PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:$PATH

panel_cava.py -f 60 -b 5 -c left > /dev/shm/cava_output_left.txt & 
panel_cava.py -f 60 -b 5 -c right > /dev/shm/cava_output_right.txt & 
panel_cava.py -f 60 -b 5 -c average > /dev/shm/cava_output.txt &
wait -n
