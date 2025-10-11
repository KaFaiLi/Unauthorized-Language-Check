import os
import pandas as pd
import whisper_timestamped as whisper
import torch
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from pydub.silence import detect_nonsilent
import numpy as np
from tqdm import tqdm
import logging
from datetime import datetime

def setup_logging(log_to_file=True, log_folder="logs"):
    """
    Setup logging configuration for progress tracking.
    
    Args:
        log_to_file (bool): Whether to save logs to a file
        log_folder (str): Folder to save log files
    """
    logger = logging.getLogger('AudioProcessor')
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_folder, f"audio_processing_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        logger.info(f"Log file created: {log_file}")
    
    return logger

def merge_contiguous_segments(segments_info, max_gap_ms=1000):
    """
    Merge contiguous flagged segments that are close together.
    
    Args:
        segments_info (list): List of segment dictionaries with flagging info
        max_gap_ms (int): Maximum gap in milliseconds to consider segments contiguous
    
    Returns:
        list: List of merged segment ranges [(start_ms, end_ms, segment_indices), ...]
    """
    if not segments_info:
        return []
    
    # Filter only flagged segments
    flagged_segments = [
        (i, seg) for i, seg in enumerate(segments_info) 
        if seg['is_flagged']
    ]
    
    if not flagged_segments:
        return []
    
    # Sort by start time
    flagged_segments.sort(key=lambda x: x[1]['start_ms'])
    
    merged = []
    current_group = [flagged_segments[0]]
    
    for i in range(1, len(flagged_segments)):
        prev_idx, prev_seg = current_group[-1]
        curr_idx, curr_seg = flagged_segments[i]
        
        # Check if current segment is close enough to previous
        gap = curr_seg['start_ms'] - prev_seg['end_ms']
        
        if gap <= max_gap_ms:
            # Merge into current group
            current_group.append(flagged_segments[i])
        else:
            # Save current group and start new one
            start_ms = current_group[0][1]['start_ms']
            end_ms = current_group[-1][1]['end_ms']
            indices = [idx for idx, _ in current_group]
            merged.append((start_ms, end_ms, indices))
            
            current_group = [flagged_segments[i]]
    
    # Add the last group
    if current_group:
        start_ms = current_group[0][1]['start_ms']
        end_ms = current_group[-1][1]['end_ms']
        indices = [idx for idx, _ in current_group]
        merged.append((start_ms, end_ms, indices))
    
    return merged

def detect_speech_segments(audio_path, min_silence_len=500, silence_thresh=-40, min_segment_len=1000):
    """
    Detect speech segments in audio file using sound wave analysis (VAD).
    
    Args:
        audio_path (str): Path to audio file
        min_silence_len (int): Minimum length of silence (in ms) to be considered as a break
        silence_thresh (int): Silence threshold in dBFS (lower = more strict)
        min_segment_len (int): Minimum length of speech segment to keep (in ms)
    
    Returns:
        list: List of tuples (start_ms, end_ms) for each speech segment
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        
        # Detect non-silent chunks (speech segments)
        speech_segments = detect_nonsilent(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        
        # Filter out very short segments
        filtered_segments = [
            (start, end) for start, end in speech_segments 
            if (end - start) >= min_segment_len
        ]
        
        return filtered_segments, audio
    
    except Exception as e:
        print(f"  - Error detecting speech segments: {e}")
        return [], None

def process_and_flag_audios(input_folder, output_excel_path, output_cropped_folder, 
                            confidence_threshold=0.7, min_silence_len=500, 
                            silence_thresh=-40, min_segment_len=1000,
                            enable_logging=True, log_folder="logs",
                            merge_flagged_segments=True, max_merge_gap_ms=1000,
                            authorized_languages=None, whisper_model_path=None,
                            model_size="large-v3-turbo"):
    """
    Processes audio files by:
    1. Using VAD to detect speech segments based on sound wave
    2. Transcribing each segment with Whisper
    3. Flagging segments based on language or confidence
    4. Merging contiguous flagged segments
    5. Saving results to Excel and flagged audio clips
    
    Args:
        input_folder (str): Path to the folder containing audio files
        output_excel_path (str): Path to save the resulting Excel file
        output_cropped_folder (str): Path to save flagged audio clips
        confidence_threshold (float): Confidence score below which a segment is flagged
        min_silence_len (int): Minimum silence length in ms for VAD
        silence_thresh (int): Silence threshold in dBFS for VAD
        min_segment_len (int): Minimum segment length in ms to keep
        enable_logging (bool): Enable logging to file
        log_folder (str): Folder to save log files
        merge_flagged_segments (bool): Merge contiguous flagged segments
        max_merge_gap_ms (int): Maximum gap to consider segments contiguous
        authorized_languages (list): List of authorized language codes (e.g., ['en', 'hi'])
        whisper_model_path (str): Custom path to Whisper model (optional)
        model_size (str): Whisper model size to use
    
    Returns:
        dict: Processing statistics and output paths
    """
    # Set default authorized languages if not provided
    if authorized_languages is None:
        authorized_languages = ["en", "hi"]
    
    # --- 1. Setup ---
    logger = setup_logging(log_to_file=enable_logging, log_folder=log_folder)
    
    if not os.path.isdir(input_folder):
        logger.error(f"The folder '{input_folder}' does not exist.")
        return {
            'success': False,
            'error': f"The folder '{input_folder}' does not exist.",
            'output_excel_path': None,
            'output_cropped_folder': None
        }

    if output_cropped_folder:
        if not os.path.isdir(output_cropped_folder):
            os.makedirs(output_cropped_folder)
            logger.info(f"Created folder for cropped audio: {output_cropped_folder}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")

    try:
        # Load model with custom path if provided
        if whisper_model_path:
            model = whisper.load_model(model_size, device=device, download_root=whisper_model_path)
            logger.info(f"Whisper model '{model_size}' loaded from custom path: {whisper_model_path}")
        else:
            model = whisper.load_model(model_size, device=device)
            logger.info(f"Whisper model '{model_size}' loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading Whisper model: {e}")
        return {
            'success': False,
            'error': str(e),
            'output_excel_path': None,
            'output_cropped_folder': None
        }

    audio_files = [f for f in os.listdir(input_folder) 
                   if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg'))]
    if not audio_files:
        logger.warning(f"No audio files found in '{input_folder}'.")
        return {
            'success': False,
            'error': f"No audio files found in '{input_folder}'.",
            'output_excel_path': None,
            'output_cropped_folder': None
        }

    logger.info(f"Found {len(audio_files)} audio file(s) to process.")
    logger.info("=" * 70)

    # --- 2. Processing with Progress Bar ---
    all_segments_data = []
    processing_stats = {
        'total_files': len(audio_files),
        'successful_files': 0,
        'failed_files': 0,
        'total_segments': 0,
        'flagged_segments': 0,
        'merged_clips': 0
    }

    # Overall file progress bar
    file_pbar = tqdm(audio_files, desc="Processing Files", unit="file", 
                     position=0, leave=True, colour='green')

    for filename in file_pbar:
        file_path = os.path.join(input_folder, filename)
        file_pbar.set_postfix_str(f"Current: {filename[:30]}...")
        logger.info(f"\nProcessing: {filename}")

        try:
            # Step 1: Detect speech segments using VAD
            logger.info(f"  Detecting speech segments using VAD...")
            speech_segments, full_audio = detect_speech_segments(
                file_path, 
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh,
                min_segment_len=min_segment_len
            )
            
            if not speech_segments:
                logger.warning(f"  No speech segments detected in {filename}")
                all_segments_data.append({
                    "Audio Filename": filename, "Start Time (s)": 0, "End Time (s)": 0,
                    "Transcription": "NO SPEECH DETECTED", "Detected Language": "N/A",
                    "Confidence Score": 0, "Is Flagged": True, 
                    "Flag Reason": "No speech segments detected"
                })
                processing_stats['failed_files'] += 1
                continue
            
            logger.info(f"  Detected {len(speech_segments)} speech segment(s)")
            
            # Temporary storage for segment info (needed for merging)
            file_segments_info = []
            
            # Step 2: Process each speech segment with Whisper
            segment_pbar = tqdm(enumerate(speech_segments), 
                              total=len(speech_segments),
                              desc=f"  Segments in {filename[:20]}", 
                              unit="seg",
                              position=1, 
                              leave=False,
                              colour='blue')
            
            for i, (start_ms, end_ms) in segment_pbar:
                start_time = start_ms / 1000.0
                end_time = end_ms / 1000.0
                
                segment_pbar.set_postfix_str(f"{start_time:.1f}s-{end_time:.1f}s")
                
                # Extract segment audio for Whisper
                segment_audio = full_audio[start_ms:end_ms]
                
                # Save temporary segment file for Whisper
                temp_segment_path = os.path.join(
                    input_folder, 
                    f"_temp_segment_{i}.wav"
                )
                segment_audio.export(temp_segment_path, format="wav")
                
                try:
                    # Transcribe with Whisper
                    audio_array = whisper.load_audio(temp_segment_path)
                    result = whisper.transcribe(model, audio_array, language=None)
                    
                    # Get transcription results
                    text = result.get("text", "").strip()
                    language = result.get("language", "unknown")
                    
                    # Calculate average confidence from all segments
                    confidence = 0.0
                    if "segments" in result and result["segments"]:
                        confidences = [seg.get("confidence", 0.0) for seg in result["segments"]]
                        confidence = np.mean(confidences) if confidences else 0.0
                    
                    # Step 3: Flag based on language or confidence
                    is_flagged = False
                    flag_reason = ""
                    
                    if language not in authorized_languages:
                        is_flagged = True
                        flag_reason = f"Language mismatch (Detected: {language})"
                    elif confidence < confidence_threshold:
                        is_flagged = True
                        flag_reason = f"Low confidence ({confidence:.2f})"
                    
                    if is_flagged:
                        processing_stats['flagged_segments'] += 1
                    
                    # Store segment info for potential merging
                    segment_info = {
                        'start_ms': start_ms,
                        'end_ms': end_ms,
                        'start_time': start_time,
                        'end_time': end_time,
                        'text': text,
                        'language': language,
                        'confidence': round(confidence, 4),
                        'is_flagged': is_flagged,
                        'flag_reason': flag_reason,
                        'segment_audio': segment_audio
                    }
                    file_segments_info.append(segment_info)
                    
                    all_segments_data.append({
                        "Audio Filename": filename,
                        "Start Time (s)": start_time,
                        "End Time (s)": end_time,
                        "Transcription": text,
                        "Detected Language": language,
                        "Confidence Score": round(confidence, 4),
                        "Is Flagged": is_flagged,
                        "Flag Reason": flag_reason if is_flagged else "N/A"
                    })
                    
                    processing_stats['total_segments'] += 1
                    
                except Exception as e:
                    logger.error(f"    Error transcribing segment {i+1}: {e}")
                    all_segments_data.append({
                        "Audio Filename": filename,
                        "Start Time (s)": start_time,
                        "End Time (s)": end_time,
                        "Transcription": "ERROR DURING TRANSCRIPTION",
                        "Detected Language": "N/A",
                        "Confidence Score": 0,
                        "Is Flagged": True,
                        "Flag Reason": f"Transcription Error: {e}"
                    })
                    processing_stats['total_segments'] += 1
                    processing_stats['flagged_segments'] += 1
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_segment_path):
                        os.remove(temp_segment_path)
            
            segment_pbar.close()
            
            # Step 4: Merge contiguous flagged segments and save
            if merge_flagged_segments and output_cropped_folder:
                logger.info(f"  Merging contiguous flagged segments...")
                merged_segments = merge_contiguous_segments(file_segments_info, max_merge_gap_ms)
                
                for merge_idx, (merge_start_ms, merge_end_ms, segment_indices) in enumerate(merged_segments):
                    try:
                        # Extract merged audio
                        merged_audio = full_audio[merge_start_ms:merge_end_ms]
                        
                        # Create filename
                        base_filename = os.path.splitext(filename)[0]
                        merged_filename = f"{base_filename}_merged_{merge_idx+1}_{merge_start_ms}ms_to_{merge_end_ms}ms.wav"
                        merged_file_path = os.path.join(output_cropped_folder, merged_filename)
                        
                        merged_audio.export(merged_file_path, format="wav")
                        processing_stats['merged_clips'] += 1
                        
                        logger.info(f"    Saved merged clip: {merged_filename} (segments: {segment_indices})")
                    except Exception as e:
                        logger.error(f"    Failed to save merged clip: {e}")
            
            elif not merge_flagged_segments and output_cropped_folder:
                # Save individual flagged segments without merging
                for seg_info in file_segments_info:
                    if seg_info['is_flagged']:
                        try:
                            base_filename = os.path.splitext(filename)[0]
                            seg_idx = file_segments_info.index(seg_info)
                            cropped_filename = f"{base_filename}_segment{seg_idx+1}_{seg_info['start_ms']}ms_to_{seg_info['end_ms']}ms.wav"
                            cropped_file_path = os.path.join(output_cropped_folder, cropped_filename)
                            seg_info['segment_audio'].export(cropped_file_path, format="wav")
                        except Exception as e:
                            logger.error(f"    Failed to save flagged segment: {e}")
            
            logger.info(f"Finished processing: {filename}")
            processing_stats['successful_files'] += 1
            
        except Exception as e:
            logger.error(f"Could not process {filename}. Error: {e}")
            all_segments_data.append({
                "Audio Filename": filename, "Start Time (s)": 0, "End Time (s)": 0,
                "Transcription": "ERROR DURING PROCESSING", "Detected Language": "N/A",
                "Confidence Score": 0, "Is Flagged": True, 
                "Flag Reason": f"Processing Error: {e}"
            })
            processing_stats['failed_files'] += 1

    file_pbar.close()

    # --- 5. Save Excel Output ---
    if not all_segments_data:
        logger.warning("No segments were processed from any audio files.")
        return {
            'success': False,
            'error': "No segments were processed from any audio files.",
            'output_excel_path': None,
            'output_cropped_folder': None
        }

    df = pd.DataFrame(all_segments_data)
    df = df[["Audio Filename", "Start Time (s)", "End Time (s)", "Is Flagged", 
             "Flag Reason", "Transcription", "Detected Language", "Confidence Score"]]

    try:
        df.to_excel(output_excel_path, index=False, engine='openpyxl')
        logger.info("\n" + "=" * 70)
        logger.info(f"✅ Successfully saved all segments to '{output_excel_path}'")
    except Exception as e:
        logger.error(f"\nError saving Excel file: {e}")
    
    # Print summary statistics
    logger.info("\n" + "=" * 70)
    logger.info("PROCESSING SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total files processed: {processing_stats['total_files']}")
    logger.info(f"  ├─ Successful: {processing_stats['successful_files']}")
    logger.info(f"  └─ Failed: {processing_stats['failed_files']}")
    logger.info(f"Total segments: {processing_stats['total_segments']}")
    logger.info(f"  ├─ Flagged: {processing_stats['flagged_segments']} ({processing_stats['flagged_segments']/max(processing_stats['total_segments'], 1)*100:.1f}%)")
    logger.info(f"  └─ Passed: {processing_stats['total_segments'] - processing_stats['flagged_segments']}")
    if merge_flagged_segments:
        logger.info(f"Merged flagged clips saved: {processing_stats['merged_clips']}")
    logger.info("=" * 70)

    # Return processing results
    return {
        'success': True,
        'output_excel_path': output_excel_path,
        'output_cropped_folder': output_cropped_folder,
        'stats': processing_stats,
        'device': device,
        'model_size': model_size,
        'authorized_languages': authorized_languages
    }

if __name__ == '__main__':
    # --- Configuration ---
    INPUT_AUDIO_FOLDER = "sample_data"
    OUTPUT_EXCEL_FILE = "output.xlsx"
    OUTPUT_CROPPED_FOLDER = "/cropped_audio"
    
    # Thresholds
    CONFIDENCE_THRESHOLD = 0.7
    
    # VAD Parameters (adjust based on your audio quality)
    MIN_SILENCE_LEN = 500      # Minimum silence length in ms
    SILENCE_THRESH = -40       # Silence threshold in dBFS (lower = stricter)
    MIN_SEGMENT_LEN = 1000     # Minimum segment length in ms
    
    # Progress & Logging
    ENABLE_LOGGING = True      # Save logs to file
    LOG_FOLDER = "logs"        # Folder for log files
    
    # Segment Merging
    MERGE_FLAGGED_SEGMENTS = True    # Merge contiguous flagged segments
    MAX_MERGE_GAP_MS = 1000          # Maximum gap (in ms) to merge segments
    
    # --- Run the main function ---
    process_and_flag_audios(
        INPUT_AUDIO_FOLDER, 
        OUTPUT_EXCEL_FILE, 
        OUTPUT_CROPPED_FOLDER,
        confidence_threshold=CONFIDENCE_THRESHOLD,
        min_silence_len=MIN_SILENCE_LEN,
        silence_thresh=SILENCE_THRESH,
        min_segment_len=MIN_SEGMENT_LEN,
        enable_logging=ENABLE_LOGGING,
        log_folder=LOG_FOLDER,
        merge_flagged_segments=MERGE_FLAGGED_SEGMENTS,
        max_merge_gap_ms=MAX_MERGE_GAP_MS
    )
