# 🔧 Installation & Troubleshooting Guide

Complete installation instructions and solutions to common issues.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Verification](#verification)
4. [Common Issues](#common-issues)
5. [Platform-Specific Instructions](#platform-specific-instructions)
6. [Advanced Configuration](#advanced-configuration)

---

## 💻 System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Python:** 3.8 or higher
- **RAM:** 8 GB
- **Storage:** 10 GB free space (for models and data)
- **Internet:** Required for initial model download

### Recommended Requirements
- **OS:** Windows 11, macOS 12+, Ubuntu 22.04+
- **Python:** 3.10 or higher
- **RAM:** 16 GB or more
- **GPU:** NVIDIA GPU with CUDA support (for faster processing)
- **Storage:** 20 GB free space

---

## 📦 Installation Steps

### Step 1: Install Python

#### Windows
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **Important:** Check "Add Python to PATH"
4. Click "Install Now"

#### macOS
```bash
# Using Homebrew
brew install python@3.10
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv
```

### Step 2: Install FFmpeg

#### Windows

**Option A: Using Chocolatey (Recommended)**
```powershell
# Install Chocolatey first (if not installed)
# Then:
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH
4. Restart terminal

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/Unauthorized-Language-Check.git
cd Unauthorized-Language-Check
```

Or download ZIP and extract.

### Step 4: Create Virtual Environment

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- streamlit
- torch
- whisper-timestamped
- pandas
- pydub
- tqdm
- openpyxl
- numpy
- And other dependencies

**Note:** PyTorch installation may take several minutes.

### Step 6: Run Setup Script

```bash
python setup.py
```

This will:
- Create necessary directories
- Verify all dependencies
- Check FFmpeg installation
- Check CUDA availability
- Create sample configuration

### Step 7: Launch Application

```bash
streamlit run app.py
```

The app should open automatically in your browser at `http://localhost:8501`

---

## ✅ Verification

### Verify Python Installation
```bash
python --version
# Should show: Python 3.8.x or higher
```

### Verify pip Installation
```bash
pip --version
# Should show pip version
```

### Verify FFmpeg Installation
```bash
ffmpeg -version
# Should show FFmpeg version and configuration
```

### Verify Virtual Environment
```bash
# Should show (venv) in your terminal prompt
# Example: (venv) PS C:\project>
```

### Verify Dependencies
```bash
python -c "import streamlit; print(streamlit.__version__)"
python -c "import torch; print(torch.__version__)"
python -c "import whisper_timestamped; print('Whisper OK')"
```

### Verify CUDA (Optional)
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

---

## 🐛 Common Issues

### Issue 1: "Python not found"

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Windows:**
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Search "Environment Variables"
   - Edit "Path" variable
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python310`

**macOS/Linux:**
```bash
# Use python3 instead of python
python3 --version
```

### Issue 2: "FFmpeg not found"

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solutions:**

**Windows:**
1. Verify installation:
   ```powershell
   where ffmpeg
   ```
2. If not found, reinstall FFmpeg
3. Add to PATH manually if needed
4. Restart terminal/IDE

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### Issue 3: "Cannot activate virtual environment"

**Symptoms (Windows):**
```
cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Symptoms (macOS/Linux):**
```
venv/bin/activate: No such file or directory
```

**Solution:**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Issue 4: "Streamlit not found"

**Symptoms:**
```
streamlit: command not found
```

**Solutions:**

1. Ensure virtual environment is activated
2. Reinstall Streamlit:
   ```bash
   pip install --upgrade streamlit
   ```
3. Use full path:
   ```bash
   python -m streamlit run app.py
   ```

### Issue 5: "PyTorch installation fails"

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement torch
```

**Solutions:**

**For CPU-only (smaller, faster install):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**For CUDA 11.8:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For CUDA 12.1:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Issue 6: "Out of memory" during processing

**Symptoms:**
```
RuntimeError: CUDA out of memory
```

**Solutions:**

1. Use smaller model:
   - Change from `large-v3` to `base` or `small`

2. Process fewer files at once

3. Close other applications

4. Use CPU instead of GPU:
   ```python
   # In main.py, force CPU:
   device = "cpu"
   ```

### Issue 7: "Whisper model download fails"

**Symptoms:**
```
Error downloading model
```

**Solutions:**

1. Check internet connection

2. Try smaller model first:
   - Start with `tiny` or `base`

3. Manual download:
   ```bash
   # Download model manually
   python -c "import whisper; whisper.load_model('base')"
   ```

4. Use custom model path in Streamlit UI

### Issue 8: "Port 8501 already in use"

**Symptoms:**
```
Address already in use
```

**Solutions:**

**Option 1: Use different port**
```bash
streamlit run app.py --server.port 8502
```

**Option 2: Kill existing process**

**Windows:**
```powershell
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:8501 | xargs kill -9
```

### Issue 9: "Audio file not recognized"

**Symptoms:**
```
CouldntDecodeError: Decoding failed
```

**Solutions:**

1. Verify FFmpeg is installed and in PATH

2. Convert audio to supported format:
   ```bash
   ffmpeg -i input.mp4 output.wav
   ```

3. Use standard formats: WAV, MP3, M4A

4. Check file is not corrupted

### Issue 10: "Excel file cannot be saved"

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'output.xlsx'
```

**Solutions:**

1. Close Excel if file is open

2. Use different filename

3. Check folder permissions

4. Run as administrator (Windows)

---

## 🖥️ Platform-Specific Instructions

### Windows 10/11

#### PowerShell Setup
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Navigate to project
cd P:\Alan\Github\Unauthorized-Language-Check

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run app
streamlit run app.py
```

#### Command Prompt Setup
```cmd
cd P:\Alan\Github\Unauthorized-Language-Check
venv\Scripts\activate.bat
streamlit run app.py
```

### macOS

#### Terminal Setup
```bash
# Navigate to project
cd ~/Projects/Unauthorized-Language-Check

# Activate virtual environment
source venv/bin/activate

# Run app
streamlit run app.py
```

#### Troubleshooting macOS
```bash
# If Python 3 not found
brew install python@3.10

# If FFmpeg not found
brew install ffmpeg

# If permission denied
chmod +x venv/bin/activate
```

### Linux (Ubuntu/Debian)

#### Terminal Setup
```bash
# Install system dependencies
sudo apt update
sudo apt install python3.10 python3-pip python3-venv ffmpeg

# Navigate to project
cd ~/Unauthorized-Language-Check

# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## 🔧 Advanced Configuration

### GPU Acceleration (NVIDIA CUDA)

#### Check CUDA Availability
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

#### Install CUDA-enabled PyTorch

**For CUDA 11.8:**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For CUDA 12.1:**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### Verify GPU Usage
```bash
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### Custom Model Path

If you want to store Whisper models in a custom location:

1. Download models manually:
   ```bash
   python -c "import whisper; whisper.load_model('large-v3-turbo', download_root='/path/to/models')"
   ```

2. In Streamlit UI:
   - Enter custom path in "Model Path" field
   - Example: `/path/to/models`

### Environment Variables

Create `.env` file:
```bash
# .env
WHISPER_MODEL_PATH=/path/to/models
DEFAULT_CONFIDENCE=0.7
DEFAULT_LANGUAGES=en,hi
```

### Proxy Configuration

If behind a corporate proxy:

```bash
# Windows
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080

# macOS/Linux
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

---

## 🧪 Testing Installation

### Quick Test Script

Create `test_installation.py`:

```python
#!/usr/bin/env python3
"""Test installation of all components."""

def test_imports():
    """Test all required imports."""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit")
    except ImportError:
        print("❌ Streamlit - NOT INSTALLED")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
        if torch.cuda.is_available():
            print(f"  ✅ CUDA: {torch.cuda.get_device_name(0)}")
        else:
            print("  ℹ️  CUDA: Not available (CPU only)")
    except ImportError:
        print("❌ PyTorch - NOT INSTALLED")
    
    try:
        import whisper_timestamped
        print("✅ Whisper Timestamped")
    except ImportError:
        print("❌ Whisper Timestamped - NOT INSTALLED")
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__}")
    except ImportError:
        print("❌ Pandas - NOT INSTALLED")
    
    try:
        from pydub import AudioSegment
        print("✅ PyDub")
    except ImportError:
        print("❌ PyDub - NOT INSTALLED")

def test_ffmpeg():
    """Test FFmpeg installation."""
    import subprocess
    print("\nTesting FFmpeg...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg: {version}")
        else:
            print("❌ FFmpeg - ERROR")
    except FileNotFoundError:
        print("❌ FFmpeg - NOT FOUND")
    except Exception as e:
        print(f"❌ FFmpeg - ERROR: {e}")

if __name__ == "__main__":
    test_imports()
    test_ffmpeg()
    print("\n✅ Installation test complete!")
```

Run test:
```bash
python test_installation.py
```

---

## 📞 Getting Help

### Documentation
- `README.md` - Overview
- `QUICKSTART.md` - Quick start guide
- `README_STREAMLIT.md` - Full documentation
- `EXAMPLES.md` - Usage examples

### Online Resources
- [Streamlit Docs](https://docs.streamlit.io/)
- [Whisper GitHub](https://github.com/openai/whisper)
- [PyTorch Docs](https://pytorch.org/docs/)
- [FFmpeg Docs](https://ffmpeg.org/documentation.html)

### Community Support
- GitHub Issues
- Stack Overflow
- Streamlit Community Forum

---

## 🎉 Success!

If you've completed all steps and tests pass, you're ready to use the Audio Language Compliance Checker!

**Next Steps:**
1. Read `QUICKSTART.md` for a quick tutorial
2. Try processing sample audio files
3. Explore the Streamlit interface
4. Check out `EXAMPLES.md` for real-world use cases

**Happy Processing! 🎧✨**
