#!/bin/zsh
# usage : ./script * 3    <- multiplies the volume by 3
#         ./script / 4   <- divides the volume by 4
#  there is a failsafe: the volume cannot be higher than 65536
#
# the snippet is originaly from there:     # awesome snippet found there: https://unix.stackexchange.com/questions/208784/command-line-per-application-volume-maybe-amixer-or-pactl
#
args=("$@")
sign=${args[1]}
factor=${args[2]}

app_name="spotify"
cur_vol=""
pactl list sink-inputs |while read line; do \
    sink_num_check=$(echo "$line" |sed -rn 's/^Sink Input #(.*)/\1/p')
    if [ "$sink_num_check" != "" ]; then
        current_sink_num="$sink_num_check"
    else
        app_name_check=$(echo "$line"  |sed -rn 's/application.name = "([^"]*)"/\1/p')
        if [ "$cur_vol" = "" ]; then
            cur_vol=$(echo "$line"  |sed -rn 's/Volume: front-left: (.*?) (.*)/\1/p' | awk '{print $1}')
        fi
        if [ "$app_name_check" = "$app_name" ]; then
            new_vol="${$(($cur_vol$sign$factor))%.*}"
            new_vol=$((new_vol<65536 ? new_vol : 65536))
            pactl set-sink-input-volume "$current_sink_num" "$new_vol"
        fi
    fi
done

