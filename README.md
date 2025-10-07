# 🎧 Audio Language & Confidence Flagging Tool

This repository contains a Python script that performs **automated audio analysis, transcription, and quality flagging** using **Whisper** and **Voice Activity Detection (VAD)**.

It is designed to:

* Detect **speech segments** automatically using waveform analysis (VAD).
* Transcribe each speech segment using **Whisper**.
* Identify **non-English or non-Hindi segments** and flag them.
* Flag segments with **low transcription confidence**.
* Optionally **merge contiguous flagged segments** and save them as cropped audio clips.
* Export a complete report to **Excel** for review and QA purposes.

---

## 🧠 Features

✅ **Automatic Speech Segmentation**
Detects and splits audio based on silent intervals using `pydub`’s VAD.

✅ **Whisper Transcription**
Transcribes each segment using the `whisper_timestamped` library with multilingual support.

✅ **Language & Confidence Flagging**
Flags:

* Non-English or non-Hindi speech
* Segments with low model confidence

✅ **Segment Merging**
Merges adjacent flagged segments within a configurable time gap (e.g., ≤ 1000 ms).

✅ **Audio Cropping & Export**
Saves flagged or merged audio clips for manual verification.

✅ **Comprehensive Logging**
Logs processing progress, warnings, and errors both in console and to a timestamped file.

✅ **Excel Report Generation**
Generates a clean, structured Excel file with:

* Audio filename
* Start & end times
* Transcription
* Detected language
* Confidence score
* Flag reason

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/audio-flagging-tool.git
cd audio-flagging-tool
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, you can create one with:

```bash
pip install pandas torch tqdm openpyxl numpy pydub whisper_timestamped
```

> 💡 You must also have **ffmpeg** installed for `pydub` to handle audio files.
> On Windows: [Download here](https://ffmpeg.org/download.html)
> On macOS (Homebrew): `brew install ffmpeg`
> On Ubuntu: `sudo apt install ffmpeg`

---

## ⚙️ Configuration

You can modify the following variables in the `__main__` section of `main.py`:

| Parameter                | Description                         | Default           |
| ------------------------ | ----------------------------------- | ----------------- |
| `INPUT_AUDIO_FOLDER`     | Folder containing input audio files | `"sample_data"`   |
| `OUTPUT_EXCEL_FILE`      | Path to save Excel results          | `"output.xlsx"`   |
| `OUTPUT_CROPPED_FOLDER`  | Folder to save cropped audio clips  | `"cropped_audio"` |
| `CONFIDENCE_THRESHOLD`   | Minimum confidence required         | `0.7`             |
| `MIN_SILENCE_LEN`        | Silence length (ms) for VAD         | `500`             |
| `SILENCE_THRESH`         | Silence threshold (dBFS)            | `-40`             |
| `MIN_SEGMENT_LEN`        | Minimum segment duration (ms)       | `1000`            |
| `ENABLE_LOGGING`         | Save logs to file                   | `True`            |
| `LOG_FOLDER`             | Folder for log files                | `"logs"`          |
| `MERGE_FLAGGED_SEGMENTS` | Merge nearby flagged segments       | `True`            |
| `MAX_MERGE_GAP_MS`       | Max gap (ms) for merging            | `1000`            |

---

## 🧩 How It Works

### 1. **Speech Detection (VAD)**

The script analyzes the waveform and splits the audio into speech segments using:

```python
detect_nonsilent(audio, min_silence_len, silence_thresh)
```

### 2. **Whisper Transcription**

Each segment is transcribed using:

```python
result = whisper.transcribe(model, audio_array)
```

The detected language and per-segment confidence are extracted.

### 3. **Flagging Logic**

A segment is **flagged** if:

* The detected language is **not English (`en`)** or **Hindi (`hi`)**, OR
* The confidence score is below `CONFIDENCE_THRESHOLD`.

### 4. **Merging Flagged Segments**

Flagged segments close together (≤ `MAX_MERGE_GAP_MS`) are merged and exported.

### 5. **Report Generation**

All processed data are stored in an Excel file with detailed per-segment metadata.

---

## 🧪 Example Output

### **Excel Columns**

| Audio Filename | Start Time (s) | End Time (s) | Transcription            | Detected Language | Confidence Score | Is Flagged | Flag Reason                      |
| -------------- | -------------- | ------------ | ------------------------ | ----------------- | ---------------- | ---------- | -------------------------------- |
| sample1.wav    | 0.0            | 8.3          | “Hello everyone…”        | en                | 0.92             | False      | N/A                              |
| sample1.wav    | 8.3            | 13.5         | “नमस्ते दोस्तों…”        | hi                | 0.88             | False      | N/A                              |
| sample1.wav    | 13.5           | 20.1         | “Bonjour tout le monde…” | fr                | 0.76             | ✅          | Language mismatch (Detected: fr) |

---

## 🚀 Run the Script

Once configured, simply run:

```bash
python main.py
```

The progress will be displayed in your terminal and logs saved in `/logs`.

---

## 📁 Output Structure

```
project/
│
├── sample_data/               # Input audio files
├── cropped_audio/             # Flagged/merged audio exports
├── logs/
│   └── audio_processing_YYYYMMDD_HHMMSS.log
│
├── output.xlsx                # Transcription & flag report
└── main.py
```

---

## 🧰 Logging Example

Console and file logs include:

```
Using device: cuda
Whisper model loaded successfully.
Processing: sample_audio.wav
  Detected 5 speech segment(s)
  Merging contiguous flagged segments...
  Saved merged clip: sample_audio_merged_1_12000ms_to_19000ms.wav
✅ Successfully saved all segments to 'output.xlsx'
```

---

## 🧱 Dependencies

| Library               | Purpose                  |
| --------------------- | ------------------------ |
| `pandas`              | Excel export             |
| `torch`               | Whisper backend          |
| `whisper_timestamped` | Transcription engine     |
| `pydub`               | Audio segmentation (VAD) |
| `tqdm`                | Progress bars            |
| `numpy`               | Confidence averaging     |
| `openpyxl`            | Excel output             |
| `logging`             | File + console logging   |

---

## 💡 Tips

* For long audios, consider adjusting `min_silence_len` and `silence_thresh` for better segmentation.
* GPU (`cuda`) support will speed up Whisper significantly.
* You can expand supported languages by editing the flag condition:

  ```python
  if language not in ["en", "hi"]:
      ...
  ```

