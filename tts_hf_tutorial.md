### Piper (The Best Balance of Quality & Performance)

This is the highly recommended method. It's almost as fast to set up, but the voice quality is excellent (neural/AI-based). It's designed to be fast and lightweight, making it perfect for a Raspberry Pi 4.

* **Pros:** Fantastic, natural-sounding voice. Very fast *inference* (generating speech). Runs fully offline.
* **Cons:** Requires Python and downloading a voice model (a one-time, ~100MB download).

#### ⚙️ How to Set Up:

1.  **Create a Python Virtual Environment (Recommended):**
    This prevents conflicts with other Python packages.
    ```bash
    python3 -m venv ~/piper-env
    source ~/piper-env/bin/activate
    ```

2.  **Install Piper:**
    Use the `pip` package manager to install it.
    ```bash
    pip install piper-tts
    ```

3.  **Download a Polish Voice Model:**
    Piper needs two files for each voice: a `.onnx` file (the model) and a `.json` file (the config). We'll download a good-quality Polish female voice ("Gosia").

    ```bash
    # Create a folder for your models
    mkdir ~/piper-models && cd ~/piper-models

    # Download the Polish voice model
    wget [https://huggingface.co/WitoldG/polish_piper_models/resolve/main/pl_PL-zenski_wg_glos-medium.onnx](https://huggingface.co/WitoldG/polish_piper_models/resolve/main/pl_PL-zenski_wg_glos-medium.onnx)
    
    # Download the model's config file
    wget [https://huggingface.co/WitoldG/polish_piper_models/resolve/main/pl_PL-zenski_wg_glos-medium.onnx.json](https://huggingface.co/WitoldG/polish_piper_models/resolve/main/pl_PL-zenski_wg_glos-medium.onnx.json)
    ```

4.  **Run Piper:**
    Now you can generate speech. The easiest way is to pipe text into it and send the audio to `aplay` (the built-in audio player).

    ```bash
    echo "To jest znacznie lepsza jakość głosu." | piper --model ~/piper-models/pl_PL-zenski_wg_glos-medium.onnx --output_file - | aplay
    ```

    * `--model`: Points to the voice model file you downloaded.
    * `--output_file -`: Tells Piper to send the audio to standard output (the "pipe").
    * `| aplay`: "Pipes" that audio directly to your speakers.

---

## Using the included example script: `test/test_tts.py`

This repository includes a ready-to-run example at `test/test_tts.py` which demonstrates how to load a Piper model in Python, synthesize WAV audio for arbitrary text, pipe it through SoX audio effects, and play via ALSA's `aplay`.

The following covers everything a first-time user needs to run and adapt that script.

### Requirements (quick)

- Python 3.8+ (use a virtualenv recommended)
- `piper-tts` Python package (provides `piper` CLI and `piper.voice.PiperVoice` module)
- system packages: `sox` and `alsa-utils` (for `aplay`). On Debian/Ubuntu: `sudo apt install sox libsox-fmt-all alsa-utils`
- a downloaded Piper ONNX model + its `.json` config in `~/piper-models` (or another folder you choose)

### Install & download (step-by-step)

1. Create and activate a venv (optional but recommended):

```bash
python3 -m venv ~/piper-env
source ~/piper-env/bin/activate
```

2. Install the Python dependency:

```bash
pip install --upgrade pip
pip install piper-tts
```

3. Install system audio tools (Debian/Ubuntu example):

```bash
sudo apt update
sudo apt install -y sox libsox-fmt-all alsa-utils
```

4. Create a models folder and download a model (example uses a Polish male voice matching the test script):

```bash
mkdir -p ~/piper-models
cd ~/piper-models
# Example model - replace the URLs with a model you prefer
wget https://huggingface.co/WitoldG/polish_piper_models/resolve/main/pl_PL-meski_wg_glos-medium.onnx
wget https://huggingface.co/WitoldG/polish_piper_models/resolve/main/pl_PL-meski_wg_glos-medium.onnx.json
```

After download you should have two files like `pl_PL-meski_wg_glos-medium.onnx` and `pl_PL-meski_wg_glos-medium.onnx.json`.

### What `test/test_tts.py` does (implementation notes)

The script demonstrates a small interactive TTS REPL. Key pieces:

- `MODEL_PATH` — a constant pointing at the model file. By default it expands `~/piper-models/pl_PL-meski_wg_glos-medium.onnx`. If you saved the model elsewhere, update this path.

- `synthesize_wav_bytes(voice: PiperVoice, text: str) -> bytes` — creates an in-memory WAV file using the Piper Python API. It opens a `wave` writer on an `io.BytesIO`, calls `voice.synthesize_wav(text, wav_file)` and returns the bytes.

- `play_wav_bytes(wav_bytes: bytes) -> None` — sets up a SoX process pipeline and `aplay`:
    - Runs SoX with the effect chain (in the example: `flanger 10 2 reverb 25 50`), reading WAV from stdin and writing WAV to stdout.
    - Pipes the SoX stdout into `aplay` which plays the audio through ALSA.
    - Writes the `wav_bytes` to SoX's stdin. If SoX or aplay are missing or misconfigured, you'll see an error (see troubleshooting below).

- `main()` — loads the model via `PiperVoice.load(MODEL_PATH)` and then runs a simple input loop. Type text and press Enter to synthesize and play; type `exit`/`quit` or Ctrl-C to stop.

### Running the example

1. Make sure your model is downloaded and `MODEL_PATH` in `test/test_tts.py` points to the `.onnx` file you picked. Two options:
        - Edit the `MODEL_PATH` constant in the file.
        - Or create a small wrapper that sets an environment variable and modify the script to read it (the script currently uses a hard-coded `MODEL_PATH`).

2. Run the script from the repo root (while your venv is active if using one):

```bash
python3 test/test_tts.py
```

You should see:

- "Loading voice model..." while the model is loaded.
- Prompt `> ` where you can type text to synthesize.

Type something like "Cześć, to jest testowy komunikat." and press Enter; the script will synthesize and play it.

### Customization and tips

- To change the voice, download a different `.onnx` + `.json` pair and change `MODEL_PATH`.
- To change audio effects, edit the `SOX_CMD` constant near the top of `test/test_tts.py`. The example uses `flanger` and `reverb`; remove them if you want raw audio.
- If you prefer to save the WAV to disk for debugging, replace the `play_wav_bytes` implementation temporarily with code that writes `wav_bytes` to a file:

```python
with open('out.wav','wb') as f:
        f.write(wav_bytes)

# then play with a local player: aplay out.wav
```

- For lower latency in interactive setups, prefer smaller models and a machine with a good CPU.

### Troubleshooting

- BrokenPipeError in `play_wav_bytes`: typically means SoX or `aplay` terminated early. Verify both are installed and work manually:

```bash
echo "test" | piper --model ~/piper-models/pl_PL-meski_wg_glos-medium.onnx --output_file - | aplay
```

- `PiperVoice.load()` fails: ensure `piper-tts` is installed in the same Python environment you're running and the model path is correct. If you see version-related errors, upgrade `piper-tts` with `pip install --upgrade piper-tts`.

- No sound from `aplay`: check ALSA works and the right output device is selected. You can test with `aplay /usr/share/sounds/alsa/Front_Center.wav` (or another WAV file).

- If you run headless or without ALSA (e.g., container without sound devices), write the WAV to disk and transfer it to a machine with audio for playback.

### Security & resource notes

- The ONNX model files are typically ~50–200MB; keep enough disk space and download over a reliable connection.
- Running synthesis is CPU-bound; on low-power boards (e.g., Raspberry Pi 4) pick a smaller model.

### Example quick checklist to get started

```bash
# create venv and install
python3 -m venv ~/piper-env && source ~/piper-env/bin/activate
pip install --upgrade pip
pip install piper-tts

# install system tools (Debian/Ubuntu)
sudo apt update && sudo apt install -y sox libsox-fmt-all alsa-utils

# download model (example shown above)
mkdir -p ~/piper-models && cd ~/piper-models
wget <model-onnx-url>
wget <model-onnx-url>.json

# run the test script
python3 test/test_tts.py
```

If you want, you can remove the SoX pipeline and play directly with `aplay` (or any other player) while you debug audio issues.

---

