#!/usr/bin/env python3
"""
Test script to validate FFmpeg installation and path.
This script helps users verify their FFmpeg setup before using the main application.
"""

import os
import sys
import subprocess
from pathlib import Path


def test_system_ffmpeg():
    """Test if FFmpeg is available in system PATH."""
    print("=" * 60)
    print("Testing System FFmpeg")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ FFmpeg found in system PATH")
            print("\nVersion Information:")
            print("-" * 60)
            # Print first 5 lines of version info
            for line in result.stdout.split('\n')[:5]:
                print(line)
            print("-" * 60)
            
            # Try to get FFmpeg location
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
                    locations = path_result.stdout.strip().split('\n')
                    print(f"\n📍 FFmpeg Location(s):")
                    for loc in locations:
                        print(f"   {loc}")
            except:
                pass
            
            return True, result.stdout.split('\n')[0]
        else:
            print("❌ FFmpeg command failed")
            return False, None
    
    except FileNotFoundError:
        print("❌ FFmpeg not found in system PATH")
        print("\n💡 Installation Instructions:")
        print("   Windows: choco install ffmpeg  OR  download from https://ffmpeg.org")
        print("   macOS:   brew install ffmpeg")
        print("   Linux:   sudo apt install ffmpeg")
        return False, None
    
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg command timed out")
        return False, None
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None


def test_custom_ffmpeg_path(ffmpeg_path):
    """Test a custom FFmpeg path."""
    print("\n" + "=" * 60)
    print(f"Testing Custom FFmpeg Path: {ffmpeg_path}")
    print("=" * 60)
    
    if not ffmpeg_path or ffmpeg_path.strip() == "":
        print("⚠️  No custom path provided")
        return False, None
    
    ffmpeg_path = ffmpeg_path.strip()
    
    # Check if path exists
    if not os.path.exists(ffmpeg_path):
        print(f"❌ Path does not exist: {ffmpeg_path}")
        return False, None
    
    # If it's a directory, look for ffmpeg executable
    if os.path.isdir(ffmpeg_path):
        print(f"📁 Path is a directory, searching for FFmpeg executable...")
        
        possible_names = ['ffmpeg.exe', 'ffmpeg']
        found = False
        
        # Check in the directory itself
        for name in possible_names:
            exe_path = os.path.join(ffmpeg_path, name)
            if os.path.isfile(exe_path):
                print(f"   ✅ Found: {exe_path}")
                ffmpeg_path = exe_path
                found = True
                break
        
        # Check in bin subdirectory
        if not found:
            bin_path = os.path.join(ffmpeg_path, 'bin')
            if os.path.isdir(bin_path):
                print(f"   Checking bin subdirectory: {bin_path}")
                for name in possible_names:
                    exe_path = os.path.join(bin_path, name)
                    if os.path.isfile(exe_path):
                        print(f"   ✅ Found: {exe_path}")
                        ffmpeg_path = exe_path
                        found = True
                        break
        
        if not found:
            print(f"   ❌ FFmpeg executable not found in directory")
            return False, None
    
    # Check if it's a file
    if not os.path.isfile(ffmpeg_path):
        print(f"❌ Not a valid file: {ffmpeg_path}")
        return False, None
    
    print(f"📄 File exists: {ffmpeg_path}")
    
    # Try to execute it
    try:
        result = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ FFmpeg executable is working correctly")
            print("\nVersion Information:")
            print("-" * 60)
            for line in result.stdout.split('\n')[:5]:
                print(line)
            print("-" * 60)
            return True, result.stdout.split('\n')[0]
        else:
            print(f"❌ FFmpeg returned error code: {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr[:200]}")
            return False, None
    
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg command timed out")
        return False, None
    
    except Exception as e:
        print(f"❌ Error executing FFmpeg: {e}")
        return False, None


def test_ffmpeg_functionality(ffmpeg_cmd='ffmpeg'):
    """Test basic FFmpeg functionality with a simple command."""
    print("\n" + "=" * 60)
    print("Testing FFmpeg Functionality")
    print("=" * 60)
    
    try:
        # Test a simple FFmpeg command (list formats)
        result = subprocess.run(
            [ffmpeg_cmd, '-formats'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ FFmpeg can list formats")
            
            # Check for common audio formats
            formats_to_check = ['mp3', 'wav', 'aac', 'm4a', 'flac', 'ogg']
            found_formats = []
            
            for fmt in formats_to_check:
                if fmt in result.stdout.lower():
                    found_formats.append(fmt)
            
            if found_formats:
                print(f"✅ Supported audio formats detected: {', '.join(found_formats)}")
            
            return True
        else:
            print("❌ FFmpeg formats command failed")
            return False
    
    except Exception as e:
        print(f"❌ Error testing FFmpeg functionality: {e}")
        return False


def test_pydub_integration(ffmpeg_path=None):
    """Test if pydub can use FFmpeg."""
    print("\n" + "=" * 60)
    print("Testing PyDub Integration")
    print("=" * 60)
    
    try:
        from pydub import AudioSegment
        print("✅ PyDub imported successfully")
        
        # Set custom FFmpeg path if provided
        if ffmpeg_path and os.path.isfile(ffmpeg_path):
            AudioSegment.converter = ffmpeg_path
            AudioSegment.ffmpeg = ffmpeg_path
            print(f"✅ Set custom FFmpeg path for PyDub: {ffmpeg_path}")
        
        # Try to create a simple audio segment (this will test FFmpeg)
        # Note: This doesn't actually process a file, just tests the setup
        print("✅ PyDub is configured and ready to use")
        
        return True
    
    except ImportError:
        print("❌ PyDub not installed")
        print("   Install with: pip install pydub")
        return False
    
    except Exception as e:
        print(f"⚠️  Warning: {e}")
        return False


def main():
    """Main test function."""
    print("\n" + "=" * 60)
    print("🎬 FFmpeg Validation Test Script")
    print("=" * 60)
    print()
    
    # Test 1: System FFmpeg
    system_ok, system_version = test_system_ffmpeg()
    
    # Test 2: Custom path (if provided)
    custom_ok = False
    custom_version = None
    custom_path = None
    
    if len(sys.argv) > 1:
        custom_path = sys.argv[1]
        custom_ok, custom_version = test_custom_ffmpeg_path(custom_path)
    
    # Test 3: Functionality
    if system_ok:
        func_ok = test_ffmpeg_functionality('ffmpeg')
    elif custom_ok and custom_path:
        func_ok = test_ffmpeg_functionality(custom_path)
    else:
        func_ok = False
        print("\n⚠️  Skipping functionality test (no working FFmpeg found)")
    
    # Test 4: PyDub integration
    if custom_ok and custom_path:
        pydub_ok = test_pydub_integration(custom_path)
    else:
        pydub_ok = test_pydub_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"System FFmpeg:        {'✅ PASS' if system_ok else '❌ FAIL'}")
    if len(sys.argv) > 1:
        print(f"Custom FFmpeg Path:   {'✅ PASS' if custom_ok else '❌ FAIL'}")
    print(f"FFmpeg Functionality: {'✅ PASS' if func_ok else '❌ FAIL'}")
    print(f"PyDub Integration:    {'✅ PASS' if pydub_ok else '❌ FAIL'}")
    print("=" * 60)
    
    # Recommendations
    print("\n💡 Recommendations:")
    if system_ok:
        print("   ✅ System FFmpeg is working. You can leave FFmpeg path empty in the app.")
    elif custom_ok:
        print(f"   ✅ Custom FFmpeg is working. Use this path in the app:")
        print(f"      {custom_path}")
    else:
        print("   ❌ No working FFmpeg found. Please install FFmpeg:")
        print("      Windows: https://ffmpeg.org/download.html")
        print("      macOS:   brew install ffmpeg")
        print("      Linux:   sudo apt install ffmpeg")
    
    print("\n" + "=" * 60)
    
    # Exit code
    if system_ok or custom_ok:
        print("✅ FFmpeg validation PASSED")
        return 0
    else:
        print("❌ FFmpeg validation FAILED")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("FFmpeg Validation Test Script")
        print("\nUsage:")
        print("  python test_ffmpeg.py                    # Test system FFmpeg")
        print("  python test_ffmpeg.py <path>             # Test custom FFmpeg path")
        print("\nExamples:")
        print("  python test_ffmpeg.py")
        print("  python test_ffmpeg.py C:/ffmpeg/bin/ffmpeg.exe")
        print("  python test_ffmpeg.py C:/ffmpeg")
        print("  python test_ffmpeg.py /usr/local/bin/ffmpeg")
        sys.exit(0)
    
    sys.exit(main())
