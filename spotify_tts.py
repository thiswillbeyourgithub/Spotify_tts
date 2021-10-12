#!/usr/bin/env python3

import subprocess
import time
import os
import sys
import psutil
from pathlib import Path

# USER SETTINGS: ###############################
High_quality_speech = True  # True for AI powered TTS, False to use espeak
rate = 23000  # default to 22000, changes the playback speed
step = 60000  # step of the model used, changing the value requires downloading
              # a different model each time, default is 95000
read_max_length = 50  # X char of title + X char of artist
espeak_cmd = f"espeak -v en -a85 -k20 -p60 -s150 --punct=''"
fade_or_pause = "fade" # if fade, will change volume while speaking
                       # if pause, will pause music while speaking
fade_level = 2 # divide the volume by 1.5 when speaking
startup_read = True # speaks aloud to tell the user that it is running
##################################################


# INITIALIZATION: ##############################
# this loop makes sure to quit if spotify is running or if another instance
# of spotify_tts is running
try:
    process_list = [" ".join(x.as_dict()["cmdline"]) for x in psutil.process_iter()]
except FileNotFoundError as e:
    print(f"Retrying because FileNotFoundError: {e}")
    process_list = [" ".join(x.as_dict()["cmdline"]) for x in psutil.process_iter()]
cnt = 0
dcnt = 0
for p in process_list:
    if "spotify" in p:
        cnt += 1
        if "tts" in p and "python" in p and "nvim" not in p:
            dcnt += 1
if dcnt > 1:
        print("Daemon already running. Exiting.")
        raise SystemExit()
if cnt-dcnt == 0:
    print("Spotify is not running. Exiting.")
    raise SystemExit()
if dcnt == 1:
    # Only 1 daemon found, so it's me, running
    pass

if startup_read is True:
    os.system(f"{espeak_cmd} 'Starting TTS'")


# Def util func: ###############################
def run_shell_cmd(cmd):
    """
    send command to the shell to execute
    """
    splitted = cmd.split(" ")
    out = subprocess.run(splitted, capture_output=True)
    return str(out.stdout)

def play_pause(order):
    """
    either pauses the music while speaking or just
    lowers the volume
    """
    if fade_or_pause == "pause":
        run_shell_cmd("playerctl --player spotify pause")
    else:
        os.chdir("../Spotify_tts/")
        if order == "play":
            os.system(f'./volume_fader.sh "*" "{fade_level}"')
        else:
            os.system(f'./volume_fader.sh "/" "{fade_level}"')

def process_text(text):
    """
    makes the title and artist more legible
    """
    text = text.replace("b'", "").replace('b"', "")
    text = text.replace("\n", "").replace("\\n", "")
    text = text.replace("\"", "").replace("'", "")
    text = text.strip().replace(".", "").replace(",", "").replace("-", ",")
    text = text.replace(" , ", ", ")
    text = text[0:read_max_length]
    text = str(text.encode("ascii", "ignore").decode())
    if "featuring" not in text:
        text = text.replace("feat", "featuring")
    return text

# Load AI libs if needed: ######################
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




# Main loop: ###################################
print("\n\nReady.")
previous_title = ""
while True:
    is_playing = run_shell_cmd("playerctl --player spotify status")
    if "Playing" in is_playing:
        title = run_shell_cmd("playerctl --player spotify metadata xesam:title")
        if title == previous_title:
            time.sleep(1)
            continue

        previous_title = title
        title = process_text(title)
        artist = run_shell_cmd("playerctl --player spotify metadata xesam:artist")
        artist = process_text(artist)

        print(f"Playing: {title}, by {artist}.")
        if High_quality_speech is False:
            play_pause("pause")
            os.system(f"{espeak_cmd} '{title} ; by {artist}.'")
            play_pause("play")
        else:
            out = model.predict(f"{title}, by {artist}.")
            wav = audio.reconstruct_waveform(out['mel'].numpy().T)
            write("output.wav", data=wav, rate=rate)
            play_pause("pause")
            playsound("output.wav")
            play_pause("play")
            Path("output.wav").unlink()
