# 🚀 Quick Start Guide

Get up and running with the Audio Language Compliance Checker in 5 minutes!

---

## ⚡ Installation (3 minutes)

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Install FFmpeg

**Windows (using Chocolatey):**
```powershell
choco install ffmpeg
```

**Or download manually from:** https://ffmpeg.org/download.html

---

## 🎯 Run the App (30 seconds)

```powershell
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📝 First-Time Setup (1 minute)

### In the Streamlit App:

1. **Select Authorized Languages** (Sidebar)
   - Choose: English, Hindi (or your preferred languages)

2. **Choose Model Size** (Sidebar)
   - Recommended: `large-v3-turbo`
   - For testing: `base` or `small`

3. **Set Input Folder** (Tab 1)
   - Enter path to your audio files
   - Example: `C:/Users/YourName/audio_files`
   - Click "🔍 Scan Folder"

4. **Configure Parameters** (Tab 2)
   - Use defaults for first run
   - Confidence Threshold: `0.7`
   - Click "💾 Save Configuration"

5. **Process Files** (Tab 3)
   - Click "🚀 Start Processing"
   - Wait for completion
   - Download results

---

## 📂 Sample Folder Structure

```
your-project/
├── sample_data/           # Your audio files here
│   ├── audio1.mp3
│   ├── audio2.wav
│   └── audio3.m4a
├── output.xlsx            # Results (generated)
├── cropped_audio/         # Flagged clips (generated)
└── logs/                  # Processing logs (generated)
```

---

## 🎬 Example Usage

### Scenario: Check call center recordings

1. **Place audio files** in `sample_data/` folder

2. **Run the app:**
   ```powershell
   streamlit run app.py
   ```

3. **Configure:**
   - Authorized Languages: English, Hindi
   - Confidence Threshold: 0.7
   - Input Folder: `sample_data`

4. **Process:**
   - Click "Start Processing"
   - Wait for completion (progress bar shows status)

5. **Review Results:**
   - Check Excel file for flagged segments
   - Listen to flagged audio clips
   - Filter by language or confidence

---

## 🔍 Understanding Results

### Excel Columns:

| Column | Meaning |
|--------|---------|
| **Is Flagged** | `True` = needs review |
| **Flag Reason** | Why it was flagged |
| **Detected Language** | Language code (en, hi, es, etc.) |
| **Confidence Score** | 0.0 to 1.0 (higher = better) |
| **Transcription** | What was said |

### Flag Reasons:

- **"Language mismatch"** - Unauthorized language detected
- **"Low confidence"** - Unclear audio or transcription
- **"No speech detected"** - Silent or no speech in file

---

## 💡 Quick Tips

### For Best Results:
- ✅ Use high-quality audio files
- ✅ Start with default parameters
- ✅ Use GPU if available (automatic)
- ✅ Process small batches first

### Common Adjustments:
- **Too many flags?** → Lower confidence threshold to 0.5
- **Missing flags?** → Raise confidence threshold to 0.8
- **Slow processing?** → Use smaller model (`base` or `small`)

---

## 🆘 Quick Troubleshooting

### App won't start?
```powershell
# Reinstall Streamlit
pip install --upgrade streamlit
streamlit run app.py
```

### No audio files detected?
- Check folder path is correct
- Ensure files are .mp3, .wav, .m4a, .flac, or .ogg

### FFmpeg error?
```powershell
# Verify FFmpeg is installed
ffmpeg -version
```

### Out of memory?
- Use smaller model size
- Process fewer files at once
- Close other applications

---

## 📚 Next Steps

- Read full documentation: `README_STREAMLIT.md`
- Customize parameters in Tab 2
- Save your configuration for reuse
- Explore filtering options in results

---

## 🎉 You're Ready!

Start processing your audio files and detecting language compliance issues!

**Need help?** Check the "📘 Tool & Usage Guide" page in the app.
