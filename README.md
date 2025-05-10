# Waydroid-SEKAI-Keybinds

My little sister who plays Project SEKAI using Memu on Windows, apparently can't stand using <a href="https://github.com/H-M-H/Weylus">Weylus</a> to play the game on Waydroid.
<br>
(honestly neither can I sometimes with the low-end tablet I have, but I've still managed to get pretty far)

So, I made a simple Python script that uses `python-evdev` and `python-uinput` to translate key presses to multi-touch events.

The default keybinds for tap notes are `Q, W, E, R, T, Y, I, O, P, [, and ]`.
<br>
The default keybinds for flick notes are `X, C, Space, Comma, and Period`.
<br>
<br>
These keys are configured to tap corresponding parts of the highway on Project SEKAI. Reconfigure the coordinates and keybinds in the code as/if needed.

So now, if for whatever reason, you're willingly playing Project SEKAI with a keyboard, you can now do it on Waydroid.
<br>
Because *someone* had to do it.

# Instructions

Minimum requirements are:
<br>
<br>
Ubuntu 20.04+ with a machine powerful enough to run Project SEKAI on Waydroid, obviously.
<br>
<br>
Dependencies are:
<br>
`python3`, `python-uinput`, `python-evdev`
<br>
<br>
Add your user to the `input` group:
<br>
`sudo usermod -aG input $USER`
<br>
`newgrp input`
<br>
<br>
Then log out of your user, and log back in.
<br>
<br>
Then just run the script with:
<br>
`python3 ./keybinds.py` (or replace "keybinds.py" with whatever you want to rename the file to)
<br>
<br>
<br>
(For the sake of saving yourself some frustration, *don't* attempt to pass any Append difficulty charts or complicated Master difficulty charts with this.)
<br>
<br>
(You have been warned, you 13 fingered aliens.)
