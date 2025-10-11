# 📂 Sample Data Folder

Place your audio files here for processing.

## Supported Formats

- `.mp3` - MP3 Audio
- `.wav` - WAV Audio
- `.m4a` - M4A/AAC Audio
- `.flac` - FLAC Audio
- `.ogg` - OGG Vorbis Audio
- `.aac` - AAC Audio
- `.wma` - Windows Media Audio

## Folder Structure

```
sample_data/
├── audio_file_1.mp3
├── audio_file_2.wav
├── interview_001.m4a
└── recording_2024.flac
```

## Tips

- Use descriptive filenames
- Ensure audio quality is good
- Keep files organized by project/date
- Avoid special characters in filenames

## Example Files

You can download sample audio files from:
- [Common Voice Dataset](https://commonvoice.mozilla.org/)
- [LibriSpeech](https://www.openslr.org/12/)
- Record your own test files

## Processing

Once files are in this folder:
1. Open the Streamlit app
2. Enter this folder path: `sample_data`
3. Click "🔍 Scan Folder"
4. Select files to process
5. Click "🚀 Start Processing"

## Output

Results will be saved to:
- `output.xlsx` - Excel report
- `cropped_audio/` - Flagged audio clips
- `logs/` - Processing logs
