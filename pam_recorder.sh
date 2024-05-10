#!/bin/bash

export PULSE_SERVER=/run/user/$(id -u phablet)/pulse/native

# check if parecord is installed
if ! [ -x "$(command -v parecord)" ]; then
    echo 'Error: parecord is not installed.' >&2
    exit 1
fi

# check if sox is installed
if ! [ -x "$(command -v sox)" ]; then
    echo 'Error: sox is not installed.' >&2
    exit 1
fi

# check if file is installed
if ! [ -x "$(command -v file)" ]; then
    echo 'Error: file is not installed.' >&2
    exit 1
fi

# Define the directory to save the recordings
SAVE_DIR="$HOME/Documents/pam_output"
LOGFILE="$SAVE_DIR/pam_recorder_log.txt"

# At the beginning of the script
START_TIME=$(date +%Y%m%d%H%M%S)
echo "Script started at $START_TIME" >> "$LOGFILE"

# Record for 1 minute
TIMESTAMP=$(date +%Y%m%d%H%M%S)
FILENAME_WAV="$SAVE_DIR/recording_$TIMESTAMP.wav"
FILENAME_FLAC="$SAVE_DIR/recording_$TIMESTAMP.flac"

# make dir only if it doesn't exist
if [ ! -d "$SAVE_DIR" ]; then
    mkdir -p "$SAVE_DIR"
fi

TIMESTAMP=$(date +%Y%m%d%H%M%S)
echo "Recording started for 1 minute... at $TIMESTAMP"
timeout 60s parecord --channels=1 "$FILENAME_WAV"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
echo "Recording saved in WAV format: $FILENAME_WAV at $TIMESTAMP"
# print it again but append timestamp
TIMESTAMP=$(date +%Y%m%d%H%M%S)
echo "Recording ended at $TIMESTAMP" >> "$LOGFILE"

# Convert WAV to FLAC using sox
TIMESTAMP=$(date +%Y%m%d%H%M%S)
echo "Converting to FLAC format... $TIMESTAMP"
/usr/bin/sox "$FILENAME_WAV" "$FILENAME_FLAC"
echo "Converted to FLAC format: $FILENAME_FLAC at $TIMESTAMP"

# Optionally, you can delete the original WAV file after conversion to save space
rm "$FILENAME_WAV"

# Check if the recording is a valid audio file
FILETYPE=$(file "$FILENAME_FLAC" | grep -oP 'audio')
if [[ -f "$FILENAME_FLAC" ]] && [[ "$FILETYPE" == "audio" ]]; then
    STATUS="success"
else
    STATUS="fail"
fi

# Log the details to the CSV log file
echo "$TIMESTAMP,$FILENAME_FLAC,$STATUS" >> "$LOGFILE"


# At the end of the script
END_TIME=$(date +%Y%m%d%H%M%S)
echo "Script ended at $END_TIME" >> "$LOGFILE"
echo "--------------------------------------------------" >> "$LOGFILE"
