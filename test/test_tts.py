import subprocess
import os
import io
import wave
from piper.voice import PiperVoice

SOX_CMD = ["sox", "-t", "wav", "-", "-t", "wav", "-", "flanger", "10", "2", "reverb", "25", "50"]
APLAY_CMD = ["aplay"]
MODEL_PATH = os.path.expanduser("~/piper-models/pl_PL-meski_wg_glos-medium.onnx")


def synthesize_wav_bytes(voice: PiperVoice, text: str) -> bytes:
    """Generate WAV bytes for the provided text."""
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    wav_buffer.seek(0)
    return wav_buffer.read()


def play_wav_bytes(wav_bytes: bytes) -> None:
    """Play WAV bytes through SoX effects into aplay."""
    p_sox = subprocess.Popen(SOX_CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p_aplay = subprocess.Popen(APLAY_CMD, stdin=p_sox.stdout)
    p_sox.stdout.close()  # Allow aplay to detect EOF

    try:
        assert p_sox.stdin is not None
        p_sox.stdin.write(wav_bytes)
        p_sox.stdin.close()
    except BrokenPipeError:
        print("Error: Audio pipeline failed. Is SoX or aplay installed?")

    p_aplay.wait()
    p_sox.wait()


def main() -> None:
    print("Loading voice model...")
    voice = PiperVoice.load(MODEL_PATH)
    print("Model loaded. Type text to synthesize (or 'exit' to quit).")

    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        text = user_input.strip()
        if not text:
            continue

        if text.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        print("Generating and playing audio...")
        wav_bytes = synthesize_wav_bytes(voice, text)
        play_wav_bytes(wav_bytes)
        print("Playback finished. Type another line or 'exit'.")


if __name__ == "__main__":
    main()