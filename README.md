# Cava for KDE Panel

<img width="682" height="79" alt="image" src="https://github.com/user-attachments/assets/aaff6fe7-8cb0-4114-9650-6b5a327b9d4d" />

## Dependencies
- `cava`
- `python`
- `bash`

## Installation
1. Download this repository:
  - Clone it using `git clone https://github.com/WinnerWind/cava-for-kdeplasma/`
  - Download it by clicking `< > Code` and downloading as ZIP.
2. Move `panel_cava.py` and `panel_cava.sh` to `~/.local/bin/`, keeping file names intact.
3. Move `panel-cava.service` to `~/.config/systemd/user/panel-cava.service`
4. Run `systemctl daemon-reload --user`
5. Start the service using `systemctl enable --now panel-cava.service --user`
6. Install the [command output widget](https://store.kde.org/p/2136636/)
7. Add the command output widget anywhere in your panel.
8. Set the command to be:
  - `tail -n 1 /dev/shm/cava_output.txt` if you want the average of both the Right and Left channels.
  - `tail -n 1 /dev/shm/cava_output_right.txt` if you just want the Right channel.
  - `tail -n 1 /dev/shm/cava_output_left.txt` if you just want the Left channel.
9. Set "Run Every" to `0ms` (You can change this if required)
10. Enable `Wait for Completion` (Required for it to work)

## Configuration
Remember to run `systemctl restart panel-cava --user` when you change configuration!

### Frame rate and Bar Count
By default, cava will run at 60 frames per second and generate 5 bars. In case you want to change this behavior, edit `~/.local/bin/panel_cava.sh` and change the lines:
```sh
FRAMERATE=60
BARS=5
```

Replacing `60` with your desired frame rate and `5` with your desired number of bars.

### Colours
You can edit the colours in the dictionary `ansi_colors` in `~/.local/bin/panel_cava.py` with your desired colours.
```py
# Edit these!
    ansi_colors = {
        'fdd': '\033[38;5;210m',  # light pink
        'fcc': '\033[38;5;217m',  # pink
        'fbb': '\033[38;5;218m',  # lighter pink
        'faa': '\033[38;5;219m',  # even lighter pink
        }
```

### Disabling Colours
You can get rid of all colours if you so desire, by commenting out these lines
```py
    ramp_list.extend(
        f'{ansi_colors.get(color.strip(" #"), "")}█{reset}'
        for color in sys.argv[2].split(',')
        if color
    )
```
... replacing it with
```py
    # ramp_list.extend(
    #     f'{ansi_colors.get(color.strip(" #"), "")}█{reset}'
    #     for color in sys.argv[2].split(',')
    #     if color
    # )
```

### Adding Spaces to Output
Replace the command used by Command Runner with (You need `perl`)
```sh
tail -n 1 /dev/shm/cava_output.txt | perl -CS -pe 's/(\e\[[0-9;]*m)|(.)/defined $1 ? $1 : "$2 "/ge; s/ $//'
```

Replace the path after the tail command with the file you want.

### Custom Colours
You can define 3-length or 6-length colors in the `EXTRA_COLORS` variable in `~/.local/bin/panel_cava.sh`. Make sure the colours are comma seperated!
*NOTE : These colours are converted to ANSI and are hence limited by the amount of colours available in ANSI* 

## Credits
- `cava` by [karlstav](https://github.com/karlstav/cava)
- Cava panel script from [milk-hyprland-rice](https://github.com/WinnerWind/milk-hyprland-rice/blob/main/Waybar/scripts/cava.py) which is from [polybar-info-cava](https://github.com/polybar/polybar-scripts/tree/master/polybar-scripts/info-cava) (Wow! A fork chain!)
