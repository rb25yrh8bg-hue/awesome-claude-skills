#!/usr/bin/env bash
# Sets up local Whisper (faster-whisper, CPU) for the watch skill. Safe to re-run.
set -e
python3 -m pip install -q --ignore-installed faster-whisper "yt-dlp[default]"
B="$HOME/.local/share/watch-faster-whisper"
mkdir -p "$B/bin" "$HOME/.config/watch"
cp "$(dirname "$0")/whisperx-faster-shim.py" "$B/bin/whisperx"; chmod +x "$B/bin/whisperx"; touch "$B/.deps-ok"
CFG="$HOME/.config/watch/.env"; touch "$CFG"
grep -q '^WATCH_WHISPERX_BIN=' "$CFG" || printf 'WATCH_ENGINE="local"\nWATCH_WHISPER_BACKEND="whisperx"\nWATCH_WHISPERX_BIN="%s"\nWATCH_WHISPERX_MODEL="small"\n' "$B/bin/whisperx" >> "$CFG"
echo "Whisper ready for watch."
