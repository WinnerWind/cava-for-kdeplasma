# Cava for KDE Panel

## Installation
1. Download this repository:
  - Clone it using `git clone https://github.com/WinnerWind/cava-for-kdeplasma/`
  - Download it by clicking `< > Code` and downloading as ZIP.
2. Move `panel_cava.py` and `panel_cava.sh` to `~/.local/bin/`, keeping file names intact.
3. Move `panel_cava.service` to `~/.config/systemd/user/panel_cava.service`
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
By default, cava will run at 60 frames per second and generate 5 bars. In case you want to change this behavior, edit `~/.local/bin/panel_cava.sh` and change the lines:
```
panel_cava.py -f 60 -b 5 -c left > /dev/shm/cava_output_left.txt & 
panel_cava.py -f 60 -b 5 -c right > /dev/shm/cava_output_right.txt & 
panel_cava.py -f 60 -b 5 -c average > /dev/shm/cava_output.txt &
```

Replacing `60` with your desired frame rate and `5` with your desired number of bars.

## Credits
- `cava` by [karlstav](https://github.com/karlstav/cava)
- Cava panel script from [milk-hyprland-rice](https://github.com/WinnerWind/milk-hyprland-rice/blob/main/Waybar/scripts/cava.py) which is from [polybar-info-cava](https://github.com/polybar/polybar-scripts/tree/master/polybar-scripts/info-cava) (Wow! A fork chain!)
