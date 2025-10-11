import streamlit as st
import os
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import sys
import subprocess
from pydub import AudioSegment
from pydub.utils import mediainfo
import torch

# Import the backend processing function
from main import process_and_flag_audios

# Page configuration
st.set_page_config(
    page_title="Audio Language Compliance Checker",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FFmpeg validation functions
def validate_ffmpeg_path(ffmpeg_path):
    """
    Validate if the provided FFmpeg path is correct and FFmpeg is functioning.
    
    Args:
        ffmpeg_path (str): Path to FFmpeg executable or directory
    
    Returns:
        tuple: (is_valid, message, version_info)
    """
    if not ffmpeg_path or ffmpeg_path.strip() == "":
        # Try system FFmpeg
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                return True, "Using system FFmpeg", version_line
            else:
                return False, "FFmpeg not found in system PATH", None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False, "FFmpeg not found in system PATH. Please provide FFmpeg path.", None
    
    # Check if path is a directory or executable
    ffmpeg_path = ffmpeg_path.strip()
    
    # If it's a directory, look for ffmpeg executable
    if os.path.isdir(ffmpeg_path):
        # Try common executable names
        possible_names = ['ffmpeg.exe', 'ffmpeg']
        for name in possible_names:
            exe_path = os.path.join(ffmpeg_path, name)
            if os.path.isfile(exe_path):
                ffmpeg_path = exe_path
                break
        else:
            # Check in bin subdirectory
            bin_path = os.path.join(ffmpeg_path, 'bin')
            if os.path.isdir(bin_path):
                for name in possible_names:
                    exe_path = os.path.join(bin_path, name)
                    if os.path.isfile(exe_path):
                        ffmpeg_path = exe_path
                        break
    
    # Check if the file exists
    if not os.path.isfile(ffmpeg_path):
        return False, f"FFmpeg executable not found at: {ffmpeg_path}", None
    
    # Try to run FFmpeg to verify it works
    try:
        result = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, f"FFmpeg is working correctly", version_line
        else:
            return False, f"FFmpeg exists but returned error code {result.returncode}", None
    
    except subprocess.TimeoutExpired:
        return False, "FFmpeg command timed out", None
    except Exception as e:
        return False, f"Error running FFmpeg: {str(e)}", None

def set_ffmpeg_path(ffmpeg_path):
    """
    Set the FFmpeg path for pydub to use.
    
    Args:
        ffmpeg_path (str): Path to FFmpeg executable
    """
    if ffmpeg_path and ffmpeg_path.strip() != "":
        ffmpeg_path = ffmpeg_path.strip()
        
        # If it's a directory, find the executable
        if os.path.isdir(ffmpeg_path):
            possible_names = ['ffmpeg.exe', 'ffmpeg']
            for name in possible_names:
                exe_path = os.path.join(ffmpeg_path, name)
                if os.path.isfile(exe_path):
                    ffmpeg_path = exe_path
                    break
            else:
                # Check in bin subdirectory
                bin_path = os.path.join(ffmpeg_path, 'bin')
                if os.path.isdir(bin_path):
                    for name in possible_names:
                        exe_path = os.path.join(bin_path, name)
                        if os.path.isfile(exe_path):
                            ffmpeg_path = exe_path
                            break
        
        # Set the path for pydub
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffmpeg = ffmpeg_path
        AudioSegment.ffprobe = ffmpeg_path.replace('ffmpeg', 'ffprobe')

# Whisper supported languages (subset of most common ones)
WHISPER_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'pl': 'Polish',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'cs': 'Czech',
    'ro': 'Romanian',
    'el': 'Greek',
    'hu': 'Hungarian',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'ms': 'Malay',
    'uk': 'Ukrainian',
    'he': 'Hebrew',
    'fa': 'Persian'
}

WHISPER_MODELS = [
    'tiny',
    'base',
    'small',
    'medium',
    'large-v3',
    'large-v3-turbo'
]

def get_audio_duration(file_path):
    """Get duration of audio file in seconds."""
    try:
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert ms to seconds
    except:
        return None

def list_audio_files(folder_path):
    """List all audio files in the specified folder with metadata."""
    if not os.path.exists(folder_path):
        return []
    
    audio_extensions = ('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma')
    audio_files = []
    
    for file in os.listdir(folder_path):
        if file.lower().endswith(audio_extensions):
            file_path = os.path.join(folder_path, file)
            duration = get_audio_duration(file_path)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            audio_files.append({
                'Filename': file,
                'Duration (s)': f"{duration:.2f}" if duration else "N/A",
                'Size (MB)': f"{size_mb:.2f}",
                'Path': file_path
            })
    
    return audio_files

def load_config():
    """Load configuration from JSON file if exists."""
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to JSON file."""
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=4)

def page_guide():
    """Page 1: Tool & Usage Guide"""
    st.title("🎧 Audio Language Compliance Checker")
    st.markdown("### 📘 Tool & Usage Guide")
    
    st.markdown("---")
    
    # Purpose
    st.header("🎯 Purpose")
    st.markdown("""
    This tool automatically analyzes audio files to detect and flag segments that:
    - Contain **unauthorized languages** (languages not in your approved list)
    - Have **low transcription confidence** (potentially unclear or problematic audio)
    
    It uses **OpenAI's Whisper** model for state-of-the-art speech recognition and language detection.
    """)
    
    # How it works
    st.header("⚙️ How It Works")
    st.markdown("""
    1. **Voice Activity Detection (VAD)**: Automatically detects speech segments in audio files
    2. **Transcription**: Uses Whisper to transcribe each speech segment
    3. **Language Detection**: Identifies the language spoken in each segment
    4. **Confidence Scoring**: Evaluates transcription quality
    5. **Flagging**: Marks segments that don't meet your criteria
    6. **Merging**: Optionally combines consecutive flagged segments
    7. **Export**: Generates Excel report and saves flagged audio clips
    """)
    
    # Key Concepts
    st.header("📚 Key Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔑 Confidence Threshold")
        st.markdown("""
        A score (0.0 to 1.0) indicating how certain the model is about its transcription.
        - **Higher values** (e.g., 0.9): Only flag very uncertain segments
        - **Lower values** (e.g., 0.5): Flag more segments for review
        - **Recommended**: 0.7
        """)
        
        st.subheader("🌍 Authorized Languages")
        st.markdown("""
        Languages that are **allowed** in your audio files. Any segment detected in a different language will be flagged.
        
        **Example**: If you select English and Hindi, any Spanish or French segments will be flagged.
        """)
    
    with col2:
        st.subheader("🚩 Flagged Segments")
        st.markdown("""
        Audio segments that are marked for review because they either:
        - Contain an **unauthorized language**
        - Have **low confidence** scores
        
        These segments are saved as separate audio clips for manual verification.
        """)
        
        st.subheader("🔗 Segment Merging")
        st.markdown("""
        Combines consecutive flagged segments that are close together (within a specified gap).
        
        **Benefits**:
        - Reduces number of output files
        - Provides better context for review
        - Saves storage space
        """)
    
    # Output Files
    st.header("📁 Expected Output Files")
    st.markdown("""
    After processing, you'll receive:
    
    1. **Excel Report** (`output.xlsx`):
       - Complete list of all segments
       - Transcriptions, languages, confidence scores
       - Flagging status and reasons
       - Timestamps for each segment
    
    2. **Flagged Audio Clips** (in `cropped_audio/` folder):
       - Individual or merged audio segments that were flagged
       - Named with timestamps for easy identification
       - WAV format for compatibility
    
    3. **Log Files** (in `logs/` folder):
       - Detailed processing logs
       - Error messages and warnings
       - Timestamped for each run
    """)
    
    # Tips
    st.header("💡 Tips for Best Results")
    st.info("""
    - **Audio Quality**: Higher quality audio produces better transcriptions
    - **Background Noise**: Adjust silence threshold if audio has noise
    - **Model Selection**: Larger models are more accurate but slower
    - **GPU Acceleration**: Use CUDA-enabled GPU for faster processing
    - **Batch Processing**: Process multiple files at once for efficiency
    """)
    
    st.markdown("---")
    st.success("Ready to get started? Go to **Main Processing** in the sidebar!")

def page_processing():
    """Page 2: Main Processing Interface"""
    st.title("🎧 Audio Language Compliance Checker")
    st.markdown("### 🚀 Main Processing Interface")
    
    # Load saved config
    config = load_config()
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Model Configuration
    st.sidebar.subheader("🤖 Whisper Model")
    
    whisper_model_path = st.sidebar.text_input(
        "Model Path (optional)",
        value=config.get('whisper_model_path', ''),
        help="Leave empty to use default system path",
        placeholder="/models/whisper"
    )
    
    model_size = st.sidebar.selectbox(
        "Model Size",
        options=WHISPER_MODELS,
        index=WHISPER_MODELS.index(config.get('model_size', 'large-v3-turbo')),
        help="Larger models are more accurate but slower"
    )
    
    # Device info
    device = "CUDA (GPU)" if torch.cuda.is_available() else "CPU"
    st.sidebar.info(f"🖥️ Device: **{device}**")
    
    st.sidebar.markdown("---")
    
    # FFmpeg Configuration
    st.sidebar.subheader("🎬 FFmpeg Configuration")
    
    ffmpeg_path = st.sidebar.text_input(
        "FFmpeg Path (optional)",
        value=config.get('ffmpeg_path', ''),
        help="Leave empty to use system FFmpeg. Provide path to FFmpeg executable or directory",
        placeholder="C:/ffmpeg/bin/ffmpeg.exe or C:/ffmpeg"
    )
    
    # Validate FFmpeg button
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        validate_ffmpeg = st.button("🔍 Validate", key="validate_ffmpeg", use_container_width=True)
    
    # Validate FFmpeg when button is clicked or on load
    if validate_ffmpeg or 'ffmpeg_validated' not in st.session_state:
        is_valid, message, version_info = validate_ffmpeg_path(ffmpeg_path)
        st.session_state['ffmpeg_valid'] = is_valid
        st.session_state['ffmpeg_message'] = message
        st.session_state['ffmpeg_version'] = version_info
        st.session_state['ffmpeg_validated'] = True
    
    # Display FFmpeg status
    if st.session_state.get('ffmpeg_valid', False):
        st.sidebar.success(f"✅ {st.session_state.get('ffmpeg_message', 'FFmpeg OK')}")
        if st.session_state.get('ffmpeg_version'):
            with st.sidebar.expander("ℹ️ FFmpeg Version"):
                st.code(st.session_state.get('ffmpeg_version', ''), language=None)
        # Set FFmpeg path for pydub
        set_ffmpeg_path(ffmpeg_path)
    else:
        st.sidebar.error(f"❌ {st.session_state.get('ffmpeg_message', 'FFmpeg not found')}")
        st.sidebar.warning("⚠️ Audio processing may fail without FFmpeg")
    
    st.sidebar.markdown("---")
    
    # Authorized Languages
    st.sidebar.subheader("🌍 Authorized Languages")
    
    default_langs = config.get('authorized_languages', ['en', 'hi'])
    authorized_languages = st.sidebar.multiselect(
        "Select Authorized Languages",
        options=list(WHISPER_LANGUAGES.keys()),
        default=default_langs,
        format_func=lambda x: f"{WHISPER_LANGUAGES[x]} ({x})",
        help="Segments in other languages will be flagged"
    )
    
    if not authorized_languages:
        st.sidebar.warning("⚠️ Please select at least one language")
    
    st.sidebar.markdown("---")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📂 Input Files", "⚙️ Parameters", "▶️ Process & Results"])
    
    with tab1:
        st.header("📂 Audio Input")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            input_folder = st.text_input(
                "Audio Folder Path",
                value=config.get('input_folder', 'sample_data'),
                help="Path to folder containing audio files",
                placeholder="C:/audio_files"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 Scan Folder", use_container_width=True):
                st.session_state['scan_folder'] = True
        
        if input_folder and (st.session_state.get('scan_folder', False) or os.path.exists(input_folder)):
            if os.path.exists(input_folder):
                audio_files = list_audio_files(input_folder)
                
                if audio_files:
                    st.success(f"✅ Found {len(audio_files)} audio file(s)")
                    
                    # Display files in a table
                    df_files = pd.DataFrame(audio_files)
                    df_display = df_files[['Filename', 'Duration (s)', 'Size (MB)']]
                    
                    st.dataframe(
                        df_display,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # File selection
                    st.markdown("---")
                    process_all = st.checkbox("Process all files", value=True)
                    
                    if not process_all:
                        selected_files = st.multiselect(
                            "Select files to process",
                            options=[f['Filename'] for f in audio_files],
                            default=[f['Filename'] for f in audio_files]
                        )
                        st.session_state['selected_files'] = selected_files
                    else:
                        st.session_state['selected_files'] = [f['Filename'] for f in audio_files]
                else:
                    st.warning("⚠️ No audio files found in the specified folder")
            else:
                st.error("❌ Folder does not exist")
    
    with tab2:
        st.header("⚙️ Processing Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Detection Parameters")
            
            confidence_threshold = st.slider(
                "Confidence Threshold",
                min_value=0.0,
                max_value=1.0,
                value=config.get('confidence_threshold', 0.7),
                step=0.05,
                help="Minimum acceptable confidence score"
            )
            
            min_silence_len = st.number_input(
                "Min Silence Length (ms)",
                min_value=100,
                max_value=2000,
                value=config.get('min_silence_len', 500),
                step=100,
                help="Minimum silence duration to split segments"
            )
            
            silence_thresh = st.number_input(
                "Silence Threshold (dBFS)",
                min_value=-60,
                max_value=-20,
                value=config.get('silence_thresh', -40),
                step=5,
                help="Lower values = stricter silence detection"
            )
            
            min_segment_len = st.number_input(
                "Min Segment Length (ms)",
                min_value=500,
                max_value=5000,
                value=config.get('min_segment_len', 1000),
                step=100,
                help="Minimum speech segment duration to keep"
            )
        
        with col2:
            st.subheader("🔗 Merging Parameters")
            
            merge_flagged_segments = st.toggle(
                "Merge Flagged Segments",
                value=config.get('merge_flagged_segments', True),
                help="Combine consecutive flagged segments"
            )
            
            max_merge_gap_ms = st.number_input(
                "Max Merge Gap (ms)",
                min_value=0,
                max_value=5000,
                value=config.get('max_merge_gap_ms', 1000),
                step=100,
                help="Maximum gap between segments to merge",
                disabled=not merge_flagged_segments
            )
            
            st.subheader("📝 Logging")
            
            enable_logging = st.toggle(
                "Enable File Logging",
                value=config.get('enable_logging', True),
                help="Save detailed logs to file"
            )
            
            log_folder = st.text_input(
                "Log Folder",
                value=config.get('log_folder', 'logs'),
                help="Folder to save log files",
                disabled=not enable_logging
            )
        
        st.markdown("---")
        
        # Output paths
        st.subheader("📁 Output Paths")
        
        col1, col2 = st.columns(2)
        
        with col1:
            output_excel_path = st.text_input(
                "Output Excel Path",
                value=config.get('output_excel_path', 'output.xlsx'),
                help="Path to save the Excel results file"
            )
        
        with col2:
            output_cropped_folder = st.text_input(
                "Cropped Audio Folder",
                value=config.get('output_cropped_folder', 'cropped_audio'),
                help="Folder to save flagged audio clips"
            )
        
        # Save configuration
        if st.button("💾 Save Configuration", use_container_width=True):
            new_config = {
                'whisper_model_path': whisper_model_path,
                'model_size': model_size,
                'ffmpeg_path': ffmpeg_path,
                'authorized_languages': authorized_languages,
                'input_folder': input_folder,
                'confidence_threshold': confidence_threshold,
                'min_silence_len': min_silence_len,
                'silence_thresh': silence_thresh,
                'min_segment_len': min_segment_len,
                'merge_flagged_segments': merge_flagged_segments,
                'max_merge_gap_ms': max_merge_gap_ms,
                'enable_logging': enable_logging,
                'log_folder': log_folder,
                'output_excel_path': output_excel_path,
                'output_cropped_folder': output_cropped_folder
            }
            save_config(new_config)
            st.success("✅ Configuration saved!")
    
    with tab3:
        st.header("▶️ Process Audio Files")
        
        # Validation
        can_process = True
        validation_messages = []
        
        if not input_folder or not os.path.exists(input_folder):
            can_process = False
            validation_messages.append("❌ Invalid input folder path")
        
        if not authorized_languages:
            can_process = False
            validation_messages.append("❌ No authorized languages selected")
        
        if not output_excel_path:
            can_process = False
            validation_messages.append("❌ Output Excel path not specified")
        
        # Check FFmpeg status
        if not st.session_state.get('ffmpeg_valid', False):
            can_process = False
            validation_messages.append("❌ FFmpeg is not configured correctly. Please validate FFmpeg path in the sidebar.")
        
        if validation_messages:
            for msg in validation_messages:
                st.error(msg)
        
        # Processing button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            start_processing = st.button(
                "🚀 Start Processing",
                disabled=not can_process,
                use_container_width=True,
                type="primary"
            )
        
        if start_processing:
            st.markdown("---")
            st.subheader("🔄 Processing Status")
            
            # Create progress containers
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_container = st.expander("📋 Processing Logs", expanded=True)
            
            with log_container:
                log_area = st.empty()
            
            try:
                # Update status
                status_text.markdown("🟠 **Status:** Processing...")
                
                # Call the backend function
                with st.spinner("Processing audio files..."):
                    result = process_and_flag_audios(
                        input_folder=input_folder,
                        output_excel_path=output_excel_path,
                        output_cropped_folder=output_cropped_folder,
                        confidence_threshold=confidence_threshold,
                        min_silence_len=min_silence_len,
                        silence_thresh=silence_thresh,
                        min_segment_len=min_segment_len,
                        enable_logging=enable_logging,
                        log_folder=log_folder,
                        merge_flagged_segments=merge_flagged_segments,
                        max_merge_gap_ms=max_merge_gap_ms,
                        authorized_languages=authorized_languages,
                        whisper_model_path=whisper_model_path if whisper_model_path else None,
                        model_size=model_size
                    )
                
                progress_bar.progress(100)
                
                if result.get('success', False):
                    status_text.markdown("🟢 **Status:** ✅ Processing Complete!")
                    
                    st.success("🎉 Processing completed successfully!")
                    
                    # Display summary statistics
                    st.markdown("---")
                    st.subheader("📊 Processing Summary")
                    
                    stats = result.get('stats', {})
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Files", stats.get('total_files', 0))
                        st.metric("Successful", stats.get('successful_files', 0))
                    
                    with col2:
                        st.metric("Failed", stats.get('failed_files', 0))
                        st.metric("Total Segments", stats.get('total_segments', 0))
                    
                    with col3:
                        flagged = stats.get('flagged_segments', 0)
                        total = stats.get('total_segments', 1)
                        flagged_pct = (flagged / total * 100) if total > 0 else 0
                        st.metric("Flagged Segments", f"{flagged} ({flagged_pct:.1f}%)")
                    
                    with col4:
                        st.metric("Merged Clips", stats.get('merged_clips', 0))
                        st.metric("Device Used", result.get('device', 'N/A'))
                    
                    # Display output paths
                    st.markdown("---")
                    st.subheader("📁 Output Files")
                    
                    st.info(f"📊 **Excel Report:** `{result.get('output_excel_path')}`")
                    st.info(f"🎵 **Flagged Audio Clips:** `{result.get('output_cropped_folder')}`")
                    
                    # Preview Excel results
                    if os.path.exists(output_excel_path):
                        st.markdown("---")
                        st.subheader("📋 Results Preview (First 20 Rows)")
                        
                        df_results = pd.read_excel(output_excel_path)
                        
                        # Add filters
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            show_flagged_only = st.checkbox("Show flagged only", value=False)
                        
                        with col2:
                            if 'Detected Language' in df_results.columns:
                                lang_filter = st.multiselect(
                                    "Filter by language",
                                    options=df_results['Detected Language'].unique(),
                                    default=[]
                                )
                        
                        with col3:
                            if 'Confidence Score' in df_results.columns:
                                min_conf = st.slider(
                                    "Min confidence",
                                    0.0, 1.0, 0.0, 0.1
                                )
                        
                        # Apply filters
                        df_filtered = df_results.copy()
                        
                        if show_flagged_only:
                            df_filtered = df_filtered[df_filtered['Is Flagged'] == True]
                        
                        if lang_filter:
                            df_filtered = df_filtered[df_filtered['Detected Language'].isin(lang_filter)]
                        
                        if 'Confidence Score' in df_filtered.columns:
                            df_filtered = df_filtered[df_filtered['Confidence Score'] >= min_conf]
                        
                        st.dataframe(
                            df_filtered.head(20),
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        st.info(f"Showing {min(20, len(df_filtered))} of {len(df_filtered)} rows (filtered from {len(df_results)} total)")
                        
                        # Download button
                        with open(output_excel_path, 'rb') as f:
                            st.download_button(
                                label="📥 Download Full Excel Report",
                                data=f,
                                file_name=os.path.basename(output_excel_path),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                else:
                    status_text.markdown("🔴 **Status:** ❌ Processing Failed")
                    st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            
            except Exception as e:
                progress_bar.progress(0)
                status_text.markdown("🔴 **Status:** ❌ Error")
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)

def main():
    """Main application entry point"""
    
    # Sidebar navigation
    st.sidebar.title("🎧 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["📘 Tool & Usage Guide", "🚀 Main Processing"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Footer
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info("""
    **Audio Language Compliance Checker**
    
    Version: 1.0.0
    
    Powered by OpenAI Whisper
    
    © 2025
    """)
    
    # Route to appropriate page
    if page == "📘 Tool & Usage Guide":
        page_guide()
    else:
        page_processing()

if __name__ == "__main__":
    main()
