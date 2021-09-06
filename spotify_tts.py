#!/usr/bin/env python3



# this simple unix-only scripts is launched at boot and reads the name of the song playing
# works only on unix
# needs to have installed playerctl

import subprocess
import time
import os
import sys


previous_song = ""
read_aloud = False
cut_limit = 50
espeak_cmd = "espeak -v en -a85 -k20 -p60 -s150 --punct=''"


def run_cmd(cmd):
    splitted = cmd.split(" ")
    out = subprocess.run(splitted, capture_output=True)
    #print(out)
    return str(out.stdout)


while True:
    is_playing = run_cmd("playerctl --player spotify status")
    if "Playing" in is_playing:
        curr_meta = run_cmd("playerctl --player spotify metadata").split("\\n")
        title = ""
        artist = ""
        for line in curr_meta:
            if "xesam:title " in line:
                title = line.split("xesam:title")[1]
                title = title.strip()
                if len(title) > cut_limit:
                    title = title[0:cut_limit]
                if title == previous_song:
                    read_aloud = False
                else:
                    read_aloud = True
            if "xesam:artist " in line:
                artist = line.split("xesam:artist")[1]
                artist = artist.strip()
                if len(artist) > cut_limit:
                    artist = artist[0:cut_limit]
        if read_aloud is True:
            run_cmd("playerctl --player spotify pause")
            print(f"Playing {title} by {artist}")
            os.system(f"{espeak_cmd} '{title}'")
            os.system(f"{espeak_cmd} 'by {artist}'")
            run_cmd("playerctl --player spotify play")
        previous_song = title
    time.sleep(2)
