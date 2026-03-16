"""Audio playback for pronunciation."""

import threading
import subprocess
import urllib.request
import tempfile
import os


def play_audio_url(url):
    """Play audio from a URL in a background thread."""
    thread = threading.Thread(target=_play, args=(url,), daemon=True)
    thread.start()


def _play(url):
    """Download and play audio."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LexiScan/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()

        # Write to temp file
        suffix = ".mp3" if ".mp3" in url else ".ogg"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(data)
            tmp_path = f.name

        try:
            # Try various audio players
            for player in ["paplay", "aplay", "mpv", "ffplay"]:
                try:
                    args = [player]
                    if player == "ffplay":
                        args.extend(["-nodisp", "-autoexit"])
                    elif player == "mpv":
                        args.append("--no-video")
                    args.append(tmp_path)

                    subprocess.run(args, capture_output=True, timeout=15)
                    break
                except FileNotFoundError:
                    continue
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        print(f"Audio playback failed: {e}")
