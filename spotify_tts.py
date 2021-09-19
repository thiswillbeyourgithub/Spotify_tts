#!/usr/bin/env python3

import subprocess
import time
import os
import sys
import psutil
from pathlib import Path

# USER SETTINGS: ###############################
High_quality_speech = True  # True for AI powered TTS, False to use espeak
rate = 22000  # default to 22000, changes the playback speed
step = 60000  # step of the model used, changing the value requires downloading
# a different model each time, default is 95000
title_max_length = 50
espeak_cmd = f"espeak -v en -a85 -k20 -p60 -s150 --punct=''"
##################################################


# this loop makes sure not to load the AI libraries if spotify is not running
process_list = [" ".join(x.as_dict()["cmdline"]) for x in psutil.process_iter()]
cnt = 0
dcnt = 0
for p in process_list:
    if "spotify" in p:
        cnt += 1
        if "tts" in p and "python" in p and "nvim" not in p:
            dcnt += 1
if dcnt == 1:
    print("Only 1 daemon found, so it's me, running.")
if dcnt > 1:
        print("Daemon already running. Exiting.")
        raise SystemExit()
if cnt-dcnt == 0:
    print("Spotify is not running. Exiting.")
    #os.system(f"{espeak_cmd} 'Spotify is not running'")
    raise SystemExit()


def run_shell_cmd(cmd):
    splitted = cmd.split(" ")
    out = subprocess.run(splitted, capture_output=True)
    return str(out.stdout)

os.system(f"{espeak_cmd} 'Starting TTS'")

if High_quality_speech is True:
    if not Path("../TransformerTTS").exists():
        print("TransformerTTS not found, downloading it using git:\n\n")
        os.chdir("..")
        os.system("git clone https://github.com/as-ideas/TransformerTTS")
    tts_dir = "/".join(os.getcwd().split("/")[0:-1]) + "/TransformerTTS"
    os.chdir(tts_dir)
    sys.path.insert(0, tts_dir)
    print(f"Temporarily added folder {tts_dir} to path.")
    from data.audio import Audio
    from model.factory import tts_ljspeech
    from scipy.io.wavfile import write
    from playsound import playsound
    model = tts_ljspeech(step)
    audio = Audio.from_config(model.config)

# initialize some values:
to_read_flag = False
previous_song = ""





print("\n\nDone initializing stuff.")
while True:
    is_playing = run_shell_cmd("playerctl --player spotify status")
    if "Playing" in is_playing:
        current_metadata = run_shell_cmd("playerctl --player spotify metadata")
        current_metadata = current_metadata.split("\\n")
        title = ""
        artist = ""
        for line in current_metadata:
            if "xesam:title " in line:
                title = line.split("xesam:title")[1]
                title = title.strip().replace(".", "").replace(",", "").replace("-", ",")
                title = title[0:title_max_length]
                if "featuring" not in title:
                    title = title.replace("feat", "featuring")

                if title == previous_song:
                    to_read_flag = False
                else:
                    to_read_flag = True
            if "xesam:artist " in line:
                artist = line.split("xesam:artist")[1]
                artist = artist.strip().replace(".", "").replace(",", "")
                if len(artist) > title_max_length:
                    artist = artist[0:title_max_length]
        if to_read_flag is True:
            print(f"Playing: {title}, by {artist}.")
            run_shell_cmd("playerctl --player spotify pause")

            if High_quality_speech is False:
                os.system(f"{espeak_cmd} '{title}, by {artist}.'")
            else:
                out = model.predict(f"{title}, by {artist}.")
                wav = audio.reconstruct_waveform(out['mel'].numpy().T)
                write("output.wav", data=wav, rate=rate)
                time.sleep(0.1)
                playsound("output.wav")
                time.sleep(0.1)

            run_shell_cmd("playerctl --player spotify play")
        previous_song = title
    time.sleep(1)
