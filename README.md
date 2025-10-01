# Unauthorized Language Check

A small Python script to transcribe audio files, detect language/confidence per-segment, flag suspicious segments (non-English/Hindi or low-confidence), export a consolidated Excel report, and optionally save cropped audio clips of flagged segments.

This repository contains a single script, `main.py`, which walks a folder of audio files, transcribes them using a Whisper-based wrapper, and writes the results to an Excel file (and cropped WAVs for flagged segments).

## What this script does
- Loads a Whisper model (via `whisper_timestamped`) and transcribes each audio file in a folder.
- For each segment, records: start/end times, transcription text, detected language, confidence score.
- Flags segments when the detected language is not English (`en`) or Hindi (`hi`), or when the confidence score is below a threshold.
- Saves all segment metadata to an Excel spreadsheet.
- Optionally crops and saves flagged audio segments as WAV files (requires `ffmpeg` for `pydub`).

## Quick start

1. Make a Python virtual environment and activate it (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
# Note: installing the appropriate `torch` wheel is best done following https://pytorch.org for your CUDA / OS setup.
```

3. Install ffmpeg on your system and ensure it's on PATH. `pydub` uses ffmpeg to read most audio formats.

4. Update paths in `main.py` before running:

- `INPUT_AUDIO_FOLDER` — folder containing your audio files (mp3, wav, m4a, flac, ogg)
- `OUTPUT_EXCEL_FILE` — path to save the Excel report (e.g. `output.xlsx`)
- `OUTPUT_CROPPED_FOLDER` — folder to save cropped flagged clips (optional)

Also optionally adjust `CONFIDENCE_THRESHOLD` and the Whisper model size used in the script (currently `base`).

5. Run the script:

```powershell
python main.py
```

## Output

- An Excel file containing one row per segment with these columns:
  - Audio Filename
  - Start Time (s)
  - End Time (s)
  - Is Flagged
  - Flag Reason
  - Transcription
  - Detected Language
  - Confidence Score
- If `OUTPUT_CROPPED_FOLDER` is set, WAV files for flagged segments will be written there.

## Dependencies / Requirements
- Python 3.8+
- See `requirements.txt` for the Python packages used by the script.
- ffmpeg (system package) required by `pydub` to read and write many audio formats.
- GPU acceleration: if you have CUDA and a compatible `torch` wheel, the script will prefer CUDA. Otherwise it falls back to CPU.

## Notes & troubleshooting
- If `pydub` raises a `CouldntDecodeError` the file could be corrupt or `ffmpeg` is missing from your PATH.
- If the Whisper model fails to load, ensure `whisper_timestamped` is installed and that `torch` is installed correctly for your platform.
- Model size: `main.py` currently calls `whisper.load_model("base")`. For faster/fewer-resources runs choose `tiny` or `small`; for better quality use `large` (requires more RAM and GPU memory).
- Excel writing uses `openpyxl` as the pandas engine.

## Customization
- Change the list of accepted languages in `main.py` (currently accepts `en` and `hi`).
- Adjust `CONFIDENCE_THRESHOLD` to be more/less strict.

## License
Proprietary to the author (no license file provided). Use and modify as needed.

---
Generated README based on `main.py`.
