2#!/bin/env python3
import argparse
import os
import signal
import subprocess
import sys
import tempfile

def hex_to_ansi256(hex_color):
    """
    Convert a 3-character hex color (like 'fdd') to the closest 256-color ANSI escape code.
    """
    if len(hex_color) == 3:
        # Expand shorthand like 'fdd' → 'ffdd'
        hex_color = ''.join([c*2 for c in hex_color])
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        return ''  # Fallback in case of malformed input

    # Convert RGB to xterm-256 color index
    def rgb_to_ansi256(r, g, b):
        # Grayscale range
        if r == g == b:
            if r < 8:
                return 16
            if r > 248:
                return 231
            return round(((r - 8) / 247) * 24) + 232
        # Color cube range
        r = round(r / 51)
        g = round(g / 51)
        b = round(b / 51)
        return 16 + (36 * r) + (6 * g) + b

    code = rgb_to_ansi256(r, g, b)
    return f'\033[38;5;{code}m'

if len(sys.argv) > 1 and sys.argv[1] == '--subproc':
    ramp_list = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

    reset = '\033[0m'

    ramp_list.extend(
        f'{hex_to_ansi256(color.strip(" #"))}█{reset}'
        for color in sys.argv[2].split(',')
        if color
    )
    while True:
        cava_input = input().strip().split()
        cava_input = [int(i) for i in cava_input]
        output = ''
        for bar in cava_input:
            if bar < len(ramp_list):
                output += ramp_list[bar]

            else:
                output += ramp_list[-1]

        print(output)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--framerate', type=int, default=60,
                    help='Framerate to be used by cava, default is 60')
parser.add_argument('-b', '--bars', type=int, default=8,
                    help='Amount of bars, default is 8')
parser.add_argument('-e', '--extra_colors', default='fdd,fcc,fbb,faa',
                    help='Color gradient used on higher values, separated by commas, default is')
parser.add_argument('-c', '--channels', choices=['stereo', 'left', 'right', 'average'],
                    help='Audio channels to be used, defaults to stereo')

opts = parser.parse_args()
conf_channels = ''
if opts.channels != 'stereo':
    conf_channels = (
        'channels=mono\n'
       f'mono_option={opts.channels}'
    )

conf_ascii_max_range = 12 + len([i for i in opts.extra_colors.split(',') if i])

cava_conf = tempfile.mkstemp('','polybar-cava-conf.')[1]
with open(cava_conf, 'w') as cava_conf_file:
    cava_conf_file.write(
        '[input]\n'
        'virtual=1\n'
        '[general]\n'
       f'framerate={opts.framerate}\n'
       f'bars={opts.bars}\n'
        '[output]\n'
        'method=raw\n'
        'data_format=ascii\n'
       f'ascii_max_range={conf_ascii_max_range}\n'
        'bar_delimiter=32\n'
        + conf_channels
    )

cava_proc = subprocess.Popen(['cava', '-p', cava_conf], stdout=subprocess.PIPE)
self_proc = subprocess.Popen(['python3', __file__, '--subproc', opts.extra_colors], stdin=cava_proc.stdout)

def cleanup(sig, frame):
    os.remove(cava_conf)
    cava_proc.kill()
    self_proc.kill()
    sys.exit(0)


signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT,  cleanup)

self_proc.wait()

