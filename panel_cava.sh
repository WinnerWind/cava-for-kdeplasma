#!/bin/bash
export PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:$PATH

FRAMERATE=60
BARS=5
EXTRA_COLORS=fdd,fcc,fbb,faa

panel_cava.py -f $FRAMERATE -b $BARS -c left -e $EXTRA_COLORS > "/dev/shm/cava_output_left.txt" &
panel_cava.py -f $FRAMERATE -b $BARS -c right -e $EXTRA_COLORS > "/dev/shm/cava_output_right.txt" &
panel_cava.py -f $FRAMERATE -b $BARS -c average -e $EXTRA_COLORS > "/dev/shm/cava_output.txt" &

wait -n
