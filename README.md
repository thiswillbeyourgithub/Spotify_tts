# Spotify_tts
**Daemon using TTS (text to speech) to read aloud the name of the music playing on spotify, vlc or other media players**

# Main points:
* Linux only, needs to have [playerctl](https://github.com/altdesktop/playerctl) installed
* 2 modes available, either poor quality speech using `espeak`, or high quality using [TransformerTTS](https://github.com/as-ideas/TransformerTTS)
* Contributions welcome.
* Can be run as daemon, using `exec --no-startup-id 'start-stop-daemon --start --background -C --pidfile /tmp/spotify_tts_pid --make-pidfile --exec /Full/path/Spotify_tts/spotify_tts.py -d /Full/path/TransformerTTS`

# Usage:
* `git clone https://github.com/thiswillbeyourgithub/Spotify_tts/`
* `cd Spotify_tts`
* `pip3 install -r ./requirements.txt` **optionnal, only if you want to use AI powered TTS**
* `cd Spotify_tts && python3 ./spotify_tts.py` 
