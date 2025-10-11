# 🎬 FFmpeg Setup Guide

Complete guide for configuring FFmpeg with the Audio Language Compliance Checker.

---

## 📋 Table of Contents

1. [What is FFmpeg?](#what-is-ffmpeg)
2. [Why is FFmpeg Required?](#why-is-ffmpeg-required)
3. [Installation Methods](#installation-methods)
4. [Configuring FFmpeg Path](#configuring-ffmpeg-path)
5. [Validation](#validation)
6. [Troubleshooting](#troubleshooting)

---

## 🎬 What is FFmpeg?

**FFmpeg** is a powerful, open-source multimedia framework that can:
- Decode, encode, transcode audio and video files
- Convert between different audio/video formats
- Extract audio from video files
- Process audio streams

Our application uses FFmpeg (via PyDub) to:
- Load and process audio files in various formats (MP3, WAV, M4A, FLAC, etc.)
- Extract audio segments for transcription
- Save processed audio clips

---

## ❓ Why is FFmpeg Required?

The Audio Language Compliance Checker **requires FFmpeg** to:

1. **Read Audio Files**: Load audio in different formats
2. **Segment Audio**: Split audio based on silence detection
3. **Export Clips**: Save flagged segments as WAV files

**Without FFmpeg, the application cannot process audio files.**

---

## 📦 Installation Methods

### Option 1: System Installation (Recommended)

#### Windows

**Method A: Using Chocolatey (Easiest)**
```powershell
# Install Chocolatey first (if not installed)
# Then run:
choco install ffmpeg
```

**Method B: Manual Installation**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Choose "Windows builds from gyan.dev"
3. Download the "release" build (ffmpeg-release-essentials.zip)
4. Extract to `C:\ffmpeg`
5. Add to System PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\ffmpeg\bin`
   - Click OK
6. Restart terminal/PowerShell

**Verify Installation:**
```powershell
ffmpeg -version
```

#### macOS

```bash
# Using Homebrew (recommended)
brew install ffmpeg

# Verify
ffmpeg -version
```

#### Linux (Ubuntu/Debian)

```bash
# Install FFmpeg
sudo apt update
sudo apt install ffmpeg

# Verify
ffmpeg -version
```

### Option 2: Portable Installation

If you don't have admin rights or prefer a portable installation:

1. Download FFmpeg (same as above)
2. Extract to any folder (e.g., `D:\Tools\ffmpeg`)
3. Note the path to `ffmpeg.exe` (e.g., `D:\Tools\ffmpeg\bin\ffmpeg.exe`)
4. Use this path in the Streamlit app (see below)

---

## ⚙️ Configuring FFmpeg Path

### In the Streamlit App

1. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

2. **Navigate to Main Processing page**

3. **In the Sidebar, find "🎬 FFmpeg Configuration"**

4. **Enter FFmpeg Path:**

   **Option A: Leave Empty (Use System FFmpeg)**
   - If FFmpeg is in your system PATH
   - Most common after standard installation
   - Just leave the field empty

   **Option B: Provide Custom Path**
   
   You can provide:
   - **Full path to executable:**
     ```
     C:\ffmpeg\bin\ffmpeg.exe
     /usr/local/bin/ffmpeg
     D:\Tools\ffmpeg\bin\ffmpeg.exe
     ```
   
   - **Path to FFmpeg directory:**
     ```
     C:\ffmpeg
     C:\ffmpeg\bin
     /usr/local/ffmpeg
     ```
   
   The app will automatically find the executable in the directory.

5. **Click "🔍 Validate" button**

6. **Check the status:**
   - ✅ Green: FFmpeg is working correctly
   - ❌ Red: FFmpeg not found or not working

7. **View version info** (click the expander if validation succeeds)

### Configuration File

FFmpeg path is saved in `config.json`:

```json
{
    "ffmpeg_path": "C:/ffmpeg/bin/ffmpeg.exe",
    ...
}
```

You can edit this file directly if needed.

---

## ✅ Validation

### Using the Streamlit App

1. Enter FFmpeg path in sidebar
2. Click "🔍 Validate"
3. Check the status message

### Using the Test Script

We provide a dedicated test script:

```bash
# Test system FFmpeg
python test_ffmpeg.py

# Test custom path
python test_ffmpeg.py "C:\ffmpeg\bin\ffmpeg.exe"
python test_ffmpeg.py "C:\ffmpeg"
python test_ffmpeg.py "/usr/local/bin/ffmpeg"
```

**The script will:**
- ✅ Check if FFmpeg exists
- ✅ Verify FFmpeg is executable
- ✅ Test FFmpeg functionality
- ✅ Check PyDub integration
- ✅ Provide recommendations

**Example Output:**
```
============================================================
🎬 FFmpeg Validation Test Script
============================================================

============================================================
Testing System FFmpeg
============================================================
✅ FFmpeg found in system PATH

Version Information:
------------------------------------------------------------
ffmpeg version 6.0 Copyright (c) 2000-2023 the FFmpeg developers
built with gcc 12.2.0 (Rev10, Built by MSYS2 project)
...
------------------------------------------------------------

📍 FFmpeg Location(s):
   C:\ProgramData\chocolatey\bin\ffmpeg.exe

============================================================
Testing FFmpeg Functionality
============================================================
✅ FFmpeg can list formats
✅ Supported audio formats detected: mp3, wav, aac, m4a, flac, ogg

============================================================
Testing PyDub Integration
============================================================
✅ PyDub imported successfully
✅ PyDub is configured and ready to use

============================================================
📊 Test Summary
============================================================
System FFmpeg:        ✅ PASS
FFmpeg Functionality: ✅ PASS
PyDub Integration:    ✅ PASS
============================================================

💡 Recommendations:
   ✅ System FFmpeg is working. You can leave FFmpeg path empty in the app.

============================================================
✅ FFmpeg validation PASSED
```

---

## 🐛 Troubleshooting

### Issue 1: "FFmpeg not found in system PATH"

**Symptoms:**
- ❌ Validation fails
- Error: "FFmpeg not found"

**Solutions:**

1. **Verify Installation:**
   ```bash
   ffmpeg -version
   ```
   
   If this fails, FFmpeg is not installed or not in PATH.

2. **Check PATH (Windows):**
   ```powershell
   $env:Path -split ';' | Select-String ffmpeg
   ```

3. **Reinstall FFmpeg** (see installation methods above)

4. **Use Custom Path:**
   - Find where FFmpeg is installed
   - Enter the path in the Streamlit app
   - Click Validate

### Issue 2: "FFmpeg exists but returned error"

**Symptoms:**
- File exists but validation fails
- Error code returned

**Solutions:**

1. **Check file permissions:**
   - Ensure the file is executable
   - On Linux/Mac: `chmod +x /path/to/ffmpeg`

2. **Verify it's the correct file:**
   ```bash
   /path/to/ffmpeg -version
   ```

3. **Check for corruption:**
   - Re-download FFmpeg
   - Extract again

### Issue 3: "Path is a directory, executable not found"

**Symptoms:**
- You provided a directory path
- App can't find the executable

**Solutions:**

1. **Provide full path to executable:**
   ```
   Instead of: C:\ffmpeg
   Use:        C:\ffmpeg\bin\ffmpeg.exe
   ```

2. **Check directory structure:**
   ```
   C:\ffmpeg\
   ├── bin\
   │   ├── ffmpeg.exe    ← This is what we need
   │   ├── ffprobe.exe
   │   └── ffplay.exe
   └── ...
   ```

3. **Verify executable exists:**
   ```powershell
   # Windows
   dir C:\ffmpeg\bin\ffmpeg.exe
   
   # Linux/Mac
   ls -l /usr/local/bin/ffmpeg
   ```

### Issue 4: "Audio processing fails even with valid FFmpeg"

**Symptoms:**
- FFmpeg validates successfully
- Audio processing still fails

**Solutions:**

1. **Check audio file format:**
   - Ensure file is a supported format
   - Try converting to WAV first

2. **Test FFmpeg manually:**
   ```bash
   ffmpeg -i your_audio.mp3 -f null -
   ```

3. **Check file permissions:**
   - Ensure app can read audio files
   - Check output folder is writable

4. **Restart the app:**
   - Close Streamlit
   - Relaunch: `streamlit run app.py`

### Issue 5: "FFmpeg works in terminal but not in app"

**Symptoms:**
- `ffmpeg -version` works in terminal
- App still can't find FFmpeg

**Solutions:**

1. **Restart the app:**
   - Environment variables may not be loaded
   - Close and reopen terminal
   - Relaunch Streamlit

2. **Use absolute path:**
   - Find FFmpeg location:
     ```bash
     # Windows
     where ffmpeg
     
     # Linux/Mac
     which ffmpeg
     ```
   - Enter this path in the app

3. **Check virtual environment:**
   - Ensure virtual environment is activated
   - FFmpeg should be accessible from venv

---

## 📝 Common FFmpeg Paths

### Windows

**Chocolatey Installation:**
```
C:\ProgramData\chocolatey\bin\ffmpeg.exe
```

**Manual Installation:**
```
C:\ffmpeg\bin\ffmpeg.exe
C:\Program Files\ffmpeg\bin\ffmpeg.exe
```

**Portable:**
```
D:\Tools\ffmpeg\bin\ffmpeg.exe
E:\Portable\ffmpeg\ffmpeg.exe
```

### macOS

**Homebrew:**
```
/usr/local/bin/ffmpeg
/opt/homebrew/bin/ffmpeg  (Apple Silicon)
```

**MacPorts:**
```
/opt/local/bin/ffmpeg
```

### Linux

**Ubuntu/Debian:**
```
/usr/bin/ffmpeg
```

**Custom Installation:**
```
/usr/local/bin/ffmpeg
/opt/ffmpeg/bin/ffmpeg
```

---

## 🧪 Testing Your Setup

### Quick Test

1. **Run the test script:**
   ```bash
   python test_ffmpeg.py
   ```

2. **Check all tests pass:**
   - System FFmpeg: ✅
   - Functionality: ✅
   - PyDub Integration: ✅

3. **If any test fails:**
   - Follow the error messages
   - Check troubleshooting section
   - Provide custom path

### Test with Custom Path

```bash
# Windows
python test_ffmpeg.py "C:\ffmpeg\bin\ffmpeg.exe"

# Linux/Mac
python test_ffmpeg.py "/usr/local/bin/ffmpeg"
```

### Manual Test

```bash
# Test FFmpeg directly
ffmpeg -version

# Test audio conversion
ffmpeg -i sample.mp3 -f null -

# Test format support
ffmpeg -formats | grep -i mp3
```

---

## 💡 Best Practices

1. **Use System Installation:**
   - Easier to maintain
   - Automatic updates
   - Works across applications

2. **Keep FFmpeg Updated:**
   ```bash
   # Windows (Chocolatey)
   choco upgrade ffmpeg
   
   # macOS (Homebrew)
   brew upgrade ffmpeg
   
   # Linux
   sudo apt update && sudo apt upgrade ffmpeg
   ```

3. **Validate After Changes:**
   - Always click "Validate" after changing path
   - Check version info
   - Test with sample audio

4. **Save Configuration:**
   - Click "💾 Save Configuration" after validation
   - Config persists across sessions

---

## 🆘 Getting Help

### If FFmpeg Still Doesn't Work:

1. **Run the test script:**
   ```bash
   python test_ffmpeg.py > ffmpeg_test_results.txt
   ```

2. **Check the output file** for detailed error messages

3. **Provide information when asking for help:**
   - Operating system and version
   - FFmpeg installation method
   - Test script output
   - Error messages from Streamlit app

### Resources

- **FFmpeg Official Site:** https://ffmpeg.org
- **FFmpeg Documentation:** https://ffmpeg.org/documentation.html
- **PyDub Documentation:** https://github.com/jiaaro/pydub

---

## ✅ Success Checklist

Before processing audio files, ensure:

- [ ] FFmpeg is installed
- [ ] FFmpeg path is configured (if needed)
- [ ] Validation shows ✅ green status
- [ ] Version info is displayed
- [ ] Configuration is saved
- [ ] Test script passes all tests

**Once all items are checked, you're ready to process audio files!** 🎉

---

**Need more help?** Check `INSTALLATION.md` for general setup or `QUICKSTART.md` for getting started.
