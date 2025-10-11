"""
Setup script for Audio Language Compliance Checker
Creates necessary directories and validates installation
"""

import os
import sys
import subprocess

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'sample_data',
        'cropped_audio',
        'logs',
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  ✅ Created: {directory}/")
        else:
            print(f"  ℹ️  Already exists: {directory}/")
    print()

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'torch',
        'pandas',
        'whisper_timestamped',
        'pydub',
        'tqdm',
        'openpyxl',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT FOUND")
            missing_packages.append(package)
    
    print()
    
    if missing_packages:
        print("⚠️  Missing packages detected!")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed!")
        return True

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("🔍 Checking FFmpeg...")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ FFmpeg found: {version_line}")
            
            # Try to get FFmpeg path
            try:
                if sys.platform == 'win32':
                    path_result = subprocess.run(
                        ['where', 'ffmpeg'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                else:
                    path_result = subprocess.run(
                        ['which', 'ffmpeg'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                
                if path_result.returncode == 0:
                    ffmpeg_location = path_result.stdout.strip().split('\n')[0]
                    print(f"  📍 Location: {ffmpeg_location}")
            except:
                pass
            
            return True
        else:
            print("  ❌ FFmpeg not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ❌ FFmpeg not found or not in PATH")
        print("  📥 Install from: https://ffmpeg.org/download.html")
        print("  💡 After installation, you can specify the FFmpeg path in the Streamlit app")
        return False
    finally:
        print()

def check_cuda():
    """Check if CUDA is available."""
    print("🔍 Checking CUDA availability...")
    
    try:
        import torch
        if torch.cuda.is_available():
            print(f"  ✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"  ℹ️  CUDA version: {torch.version.cuda}")
            return True
        else:
            print("  ℹ️  CUDA not available - will use CPU")
            print("  💡 For faster processing, install CUDA-enabled PyTorch")
            return False
    except ImportError:
        print("  ⚠️  PyTorch not installed")
        return False
    finally:
        print()

def create_sample_config():
    """Create a sample configuration file if it doesn't exist."""
    config_file = 'config.json'
    
    if not os.path.exists(config_file):
        print(f"📝 Creating sample configuration: {config_file}")
        
        import json
        
        sample_config = {
            "whisper_model_path": "",
            "model_size": "large-v3-turbo",
            "ffmpeg_path": "",
            "authorized_languages": ["en", "hi"],
            "input_folder": "sample_data",
            "confidence_threshold": 0.7,
            "min_silence_len": 500,
            "silence_thresh": -40,
            "min_segment_len": 1000,
            "merge_flagged_segments": True,
            "max_merge_gap_ms": 1000,
            "enable_logging": True,
            "log_folder": "logs",
            "output_excel_path": "output.xlsx",
            "output_cropped_folder": "cropped_audio"
        }
        
        with open(config_file, 'w') as f:
            json.dump(sample_config, f, indent=4)
        
        print(f"  ✅ Created: {config_file}")
    else:
        print(f"  ℹ️  Configuration already exists: {config_file}")
    
    print()

def print_summary(deps_ok, ffmpeg_ok):
    """Print setup summary."""
    print("=" * 60)
    print("📊 SETUP SUMMARY")
    print("=" * 60)
    
    if deps_ok and ffmpeg_ok:
        print("✅ Setup complete! You're ready to go!")
        print()
        print("🚀 To start the app, run:")
        print("   streamlit run app.py")
        print()
        print("📚 For help, see:")
        print("   - QUICKSTART.md")
        print("   - README_STREAMLIT.md")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
        print()
        if not deps_ok:
            print("📦 Install dependencies:")
            print("   pip install -r requirements.txt")
        if not ffmpeg_ok:
            print("🎬 Install FFmpeg:")
            print("   https://ffmpeg.org/download.html")
    
    print("=" * 60)

def main():
    """Main setup function."""
    print("=" * 60)
    print("🎧 Audio Language Compliance Checker - Setup")
    print("=" * 60)
    print()
    
    # Create directories
    create_directories()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    # Check CUDA
    check_cuda()
    
    # Create sample config
    create_sample_config()
    
    # Print summary
    print_summary(deps_ok, ffmpeg_ok)

if __name__ == "__main__":
    main()
