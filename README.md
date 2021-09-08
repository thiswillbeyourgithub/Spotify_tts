# Spotify_tts
**Daemon using TTS (text to speech) to read aloud the name of the music playing on spotify, vlc or other media players**

# Main points:
* Linux only, needs to have [playerctl](https://github.com/altdesktop/playerctl) installed
* 2 modes available, either poor quality speech using `espeak`, or high quality using [TransformerTTS](https://github.com/as-ideas/TransformerTTS)
* Contributions welcome.
* My crontab is something as follow: 
```
*/5 * * * * start-stop-daemon  --pidfile /tmp/spotify_tts_pid --make-pidfile --background --start --exec /PATH/spotify_tts.py -d /PATH/TransformerTTS
59 * * * * kill $(pgrep --full "spotify_tts.py")
```


# Usage:
* `git clone https://github.com/thiswillbeyourgithub/Spotify_tts/`
* `cd Spotify_tts`
* `pip3 install -r ./requirements.txt` **optionnal, only if you want to use AI powered TTS**
* `cd Spotify_tts && python3 ./spotify_tts.py`  to launch it directly, otherwise run it as daemon like shown above
