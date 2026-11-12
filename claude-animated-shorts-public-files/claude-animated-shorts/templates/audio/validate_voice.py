#!/usr/bin/env python3
"""Inspect voice.wav and optionally validate word-level words.json."""
import argparse
import json
import wave
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voice", nargs="?", default="voice/voice.wav")
    ap.add_argument("--words", default="voice/words.json")
    args = ap.parse_args()
    voice = Path(args.voice)
    if not voice.exists():
        raise SystemExit(f"ERROR: voice file not found: {voice}")
    try:
        with wave.open(str(voice), "rb") as w:
            channels = w.getnchannels()
            rate = w.getframerate()
            frames = w.getnframes()
            width = w.getsampwidth()
            duration = frames / float(rate)
    except wave.Error as e:
        raise SystemExit(f"ERROR: unsupported or invalid WAV: {e}")
    print(f"Voice: {voice}")
    print(f"Duration: {duration:.3f} seconds")
    print(f"Sample rate: {rate} Hz")
    print(f"Channels: {channels}")
    print(f"Sample width: {width * 8}-bit")
    if rate != 48000:
        print("WARNING: expected 48000 Hz for the supplied audio pipeline.")
    if channels not in (1, 2):
        print("WARNING: expected mono or stereo audio.")
    words_path = Path(args.words)
    if words_path.exists():
        try:
            words = json.loads(words_path.read_text(encoding="utf-8"))
        except Exception as e:
            raise SystemExit(f"ERROR: cannot parse {words_path}: {e}")
        if not isinstance(words, list):
            raise SystemExit("ERROR: words.json must contain a JSON array.")
        previous_start = -1.0
        for i, item in enumerate(words):
            if not isinstance(item, dict) or not all(k in item for k in ("word", "s", "e")):
                raise SystemExit(f"ERROR: word item {i} must contain word, s, e.")
            s, e = float(item["s"]), float(item["e"])
            if s < 0 or e <= s or e > duration + 0.25:
                raise SystemExit(f"ERROR: invalid timing at item {i}: {s} - {e}")
            if s < previous_start:
                raise SystemExit(f"ERROR: word timings are not ordered at item {i}.")
            previous_start = s
        print(f"Word timings: {len(words)} entries, format OK")
    else:
        print(f"Word timings: not found at {words_path}")
    print("Validation complete.")

if __name__ == "__main__":
    main()
