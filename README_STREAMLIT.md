# 🎧 Audio Language Compliance Checker - Streamlit Web App

A powerful web-based application for automated audio analysis, transcription, and language compliance checking using **OpenAI Whisper** and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green)

---

## 🌟 Features

### 🎯 Core Capabilities
- ✅ **Automatic Speech Detection** - VAD-based speech segmentation
- ✅ **Multi-language Transcription** - Powered by Whisper AI
- ✅ **Language Compliance Checking** - Flag unauthorized languages
- ✅ **Confidence Scoring** - Identify low-quality transcriptions
- ✅ **Segment Merging** - Combine consecutive flagged segments
- ✅ **Audio Export** - Save flagged clips for review
- ✅ **Excel Reporting** - Comprehensive results in spreadsheet format

### 🖥️ Web Interface Features
- 📊 **Interactive Dashboard** - User-friendly Streamlit interface
- 🎛️ **Configurable Parameters** - Adjust all settings via UI
- 📁 **File Browser** - View and select audio files
- 📈 **Real-time Progress** - Live processing updates
- 📋 **Results Preview** - Filter and explore results
- 💾 **Configuration Persistence** - Save/load settings
- 🎨 **Modern UI** - Clean, professional design

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio processing)
- CUDA-capable GPU (optional, for faster processing)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Unauthorized-Language-Check.git
cd Unauthorized-Language-Check
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install FFmpeg

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract and add to PATH

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 🚀 Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Using the Command Line (Legacy)

You can still use the original command-line interface:

```bash
python main.py
```

---

## 📖 User Guide

### Page 1: Tool & Usage Guide

This page provides:
- 🎯 Purpose and overview
- ⚙️ How the tool works
- 📚 Key concepts and definitions
- 📁 Expected output files
- 💡 Tips for best results

### Page 2: Main Processing Interface

#### Tab 1: Input Files 📂

1. **Enter Audio Folder Path**
   - Specify the folder containing your audio files
   - Click "🔍 Scan Folder" to detect files

2. **Review Detected Files**
   - View list of audio files with duration and size
   - Select specific files or process all

#### Tab 2: Parameters ⚙️

**Detection Parameters:**
- **Confidence Threshold** (0.0 - 1.0): Minimum acceptable confidence
  - Default: 0.7
  - Higher = stricter quality requirements

- **Min Silence Length** (ms): Silence duration to split segments
  - Default: 500ms
  - Adjust based on audio characteristics

- **Silence Threshold** (dBFS): Silence detection sensitivity
  - Default: -40 dBFS
  - Lower values = stricter detection

- **Min Segment Length** (ms): Minimum speech segment duration
  - Default: 1000ms
  - Filters out very short segments

**Merging Parameters:**
- **Merge Flagged Segments**: Combine consecutive flagged segments
  - Default: Enabled
  - Reduces number of output files

- **Max Merge Gap** (ms): Maximum gap to merge segments
  - Default: 1000ms
  - Only applies when merging is enabled

**Output Paths:**
- **Output Excel Path**: Where to save the results spreadsheet
- **Cropped Audio Folder**: Where to save flagged audio clips

#### Tab 3: Process & Results ▶️

1. **Click "🚀 Start Processing"**
   - Validates all inputs
   - Shows real-time progress
   - Displays processing logs

2. **View Results**
   - Processing summary statistics
   - Output file locations
   - Preview first 20 rows of results
   - Filter by flagged status, language, or confidence

3. **Download Results**
   - Click "📥 Download Full Excel Report"
   - Access flagged audio clips in the output folder

---

## 🎛️ Sidebar Configuration

### Whisper Model Settings

**Model Path** (optional):
- Leave empty to use default system path
- Specify custom path if models are stored elsewhere

**Model Size**:
- `tiny` - Fastest, least accurate
- `base` - Fast, basic accuracy
- `small` - Balanced
- `medium` - Good accuracy, slower
- `large-v3` - Best accuracy, slowest
- `large-v3-turbo` - **Recommended** - Best balance

### Authorized Languages

Select one or more languages that are **allowed** in your audio:
- English (en)
- Hindi (hi)
- Spanish (es)
- French (fr)
- German (de)
- Japanese (ja)
- Korean (ko)
- And 20+ more...

Any segment detected in a non-authorized language will be flagged.

---

## 📁 Output Files

### 1. Excel Report (`output.xlsx`)

Contains columns:
- **Audio Filename**: Source file name
- **Start Time (s)**: Segment start timestamp
- **End Time (s)**: Segment end timestamp
- **Is Flagged**: Boolean flag status
- **Flag Reason**: Why segment was flagged
- **Transcription**: Text transcription
- **Detected Language**: Language code
- **Confidence Score**: Model confidence (0-1)

### 2. Flagged Audio Clips (`cropped_audio/`)

Naming format:
```
{original_filename}_merged_{index}_{start_ms}ms_to_{end_ms}ms.wav
```

Example:
```
interview_001_merged_1_5000ms_to_12000ms.wav
```

### 3. Log Files (`logs/`)

Naming format:
```
audio_processing_{timestamp}.log
```

Contains:
- Processing progress
- Detected segments
- Errors and warnings
- Summary statistics

---

## ⚙️ Configuration File

Settings are automatically saved to `config.json`:

```json
{
    "whisper_model_path": "",
    "model_size": "large-v3-turbo",
    "authorized_languages": ["en", "hi"],
    "input_folder": "sample_data",
    "confidence_threshold": 0.7,
    "min_silence_len": 500,
    "silence_thresh": -40,
    "min_segment_len": 1000,
    "merge_flagged_segments": true,
    "max_merge_gap_ms": 1000,
    "enable_logging": true,
    "log_folder": "logs",
    "output_excel_path": "output.xlsx",
    "output_cropped_folder": "cropped_audio"
}
```

---

## 💡 Tips & Best Practices

### Audio Quality
- Use high-quality audio files (WAV, FLAC preferred)
- Minimize background noise
- Ensure clear speech

### Model Selection
- **For speed**: Use `base` or `small`
- **For accuracy**: Use `large-v3-turbo` or `large-v3`
- **For testing**: Use `tiny` or `base`

### Parameter Tuning

**If too many segments are flagged:**
- Lower confidence threshold (e.g., 0.5)
- Increase silence threshold (e.g., -35 dBFS)

**If segments are missed:**
- Raise confidence threshold (e.g., 0.8)
- Decrease silence threshold (e.g., -45 dBFS)
- Reduce min segment length

### Performance Optimization
- Use GPU (CUDA) for 5-10x faster processing
- Process files in batches
- Use smaller models for large datasets
- Enable segment merging to reduce output files

---

## 🐛 Troubleshooting

### Common Issues

**"No audio files found"**
- Check folder path is correct
- Ensure files have supported extensions (.mp3, .wav, .m4a, .flac, .ogg)

**"Error loading Whisper model"**
- Check internet connection (first download)
- Verify sufficient disk space
- Try a smaller model size

**"FFmpeg not found"**
- Install FFmpeg and add to system PATH
- Restart terminal/IDE after installation

**Slow processing**
- Use GPU if available
- Select smaller model
- Reduce audio file quality/length

**High memory usage**
- Process fewer files at once
- Use smaller model
- Close other applications

---

## 🔧 Advanced Usage

### Custom Language Detection

Edit `app.py` to add more languages to `WHISPER_LANGUAGES` dictionary:

```python
WHISPER_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'your_lang': 'Your Language',
    # ... add more
}
```

### Batch Processing Script

Create a script to process multiple folders:

```python
from main import process_and_flag_audios

folders = ['folder1', 'folder2', 'folder3']

for folder in folders:
    process_and_flag_audios(
        input_folder=folder,
        output_excel_path=f"{folder}_results.xlsx",
        output_cropped_folder=f"{folder}_flagged",
        # ... other parameters
    )
```

---

## 📊 Example Workflow

1. **Prepare Audio Files**
   - Collect audio files in a folder
   - Ensure consistent quality

2. **Launch App**
   ```bash
   streamlit run app.py
   ```

3. **Configure Settings**
   - Select authorized languages
   - Adjust confidence threshold
   - Set output paths

4. **Scan & Select Files**
   - Enter folder path
   - Review detected files
   - Select files to process

5. **Process**
   - Click "Start Processing"
   - Monitor progress
   - Review logs

6. **Review Results**
   - Check summary statistics
   - Preview Excel results
   - Filter flagged segments

7. **Download & Verify**
   - Download Excel report
   - Listen to flagged audio clips
   - Take corrective action

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **OpenAI Whisper** - State-of-the-art speech recognition
- **Streamlit** - Beautiful web app framework
- **PyDub** - Audio processing library

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: your.email@example.com

---

## 🔄 Version History

### v1.0.0 (2025-01-XX)
- Initial release
- Streamlit web interface
- Multi-language support
- Configurable parameters
- Excel reporting
- Audio clip export

---

**Made with ❤️ using Python, Whisper, and Streamlit**
