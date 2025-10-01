import os
import pandas as pd
import whisper_timestamped as whisper
import torch
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def process_and_flag_audios(input_folder, output_excel_path, output_cropped_folder, confidence_threshold=0.7):
    """
    Processes all audio files in a folder, flags segments based on language or confidence,
    saves all segment information to an Excel file, and saves flagged audio clips to a separate folder.

    Args:
        input_folder (str): Path to the folder containing audio files.
        output_excel_path (str): Path to save the resulting Excel file.
        output_cropped_folder (str): Path to the folder to save flagged audio clips.
        confidence_threshold (float): Confidence score below which a segment is flagged.
    """
    # --- 1. Setup ---
    # Validate input and create output directories
    if not os.path.isdir(input_folder):
        print(f"Error: The folder '{input_folder}' does not exist.")
        return

    if output_cropped_folder:
        if not os.path.isdir(output_cropped_folder):
            os.makedirs(output_cropped_folder)
            print(f"Created folder for cropped audio: {output_cropped_folder}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    try:
        model = whisper.load_model("base", device=device)
        print("Whisper model loaded successfully.")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        return

    audio_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg'))]
    if not audio_files:
        print(f"No audio files found in '{input_folder}'.")
        return

    print(f"Found {len(audio_files)} audio file(s) to process.")

    # --- 2. Processing ---
    all_segments_data = []

    for filename in audio_files:
        file_path = os.path.join(input_folder, filename)
        print(f"\nProcessing: {filename}...")

        # Load audio with pydub for cropping. This is done once per file.
        full_audio_for_cropping = None
        if output_cropped_folder:
            try:
                full_audio_for_cropping = AudioSegment.from_file(file_path)
            except CouldntDecodeError:
                print(f"  - Warning: Could not decode {filename} with pydub. FFmpeg might be missing or the file is corrupt. Skipping cropping for this file.")
            except Exception as e:
                print(f"  - Warning: Could not load {filename} with pydub for cropping. Error: {e}")

        try:
            # Transcribe with Whisper
            audio = whisper.load_audio(file_path)
            result = whisper.transcribe(model, audio, language=None)

            # --- 3. Analysis, Flagging, and Cropping ---
            for i, segment in enumerate(result["segments"]):
                language = segment.get("language", "unknown")
                confidence = segment.get("confidence", 0.0)
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"].strip()

                is_flagged = False
                flag_reason = ""

                if language not in ["en", "hi"]:
                    is_flagged = True
                    flag_reason = f"Language mismatch (Detected: {language})"
                elif confidence < confidence_threshold:
                    is_flagged = True
                    flag_reason = f"Low confidence ({confidence:.2f})"

                # --- New Feature: Crop and Save Flagged Audio ---
                if is_flagged and full_audio_for_cropping:
                    try:
                        start_ms = int(start_time * 1000)
                        end_ms = int(end_time * 1000)
                        cropped_clip = full_audio_for_cropping[start_ms:end_ms]

                        base_filename = os.path.splitext(filename)[0]
                        cropped_filename = f"{base_filename}_segment{i+1}_{start_ms}ms_to_{end_ms}ms.wav"
                        cropped_file_path = os.path.join(output_cropped_folder, cropped_filename)

                        cropped_clip.export(cropped_file_path, format="wav")
                    except Exception as e:
                        print(f"    - Failed to crop segment from {start_time:.2f}s to {end_time:.2f}s. Error: {e}")
                # --- End of New Feature ---

                all_segments_data.append({
                    "Audio Filename": filename,
                    "Start Time (s)": start_time,
                    "End Time (s)": end_time,
                    "Transcription": text,
                    "Detected Language": language,
                    "Confidence Score": confidence,
                    "Is Flagged": is_flagged,
                    "Flag Reason": flag_reason if is_flagged else "N/A"
                })
            print(f"Finished processing: {filename}")

        except Exception as e:
            print(f"Could not process {filename} with Whisper. Error: {e}")
            all_segments_data.append({
                "Audio Filename": filename, "Start Time (s)": 0, "End Time (s)": 0,
                "Transcription": "ERROR DURING PROCESSING", "Detected Language": "N/A",
                "Confidence Score": 0, "Is Flagged": True, "Flag Reason": f"Processing Error: {e}"
            })

    # --- 4. Saving the Excel Output ---
    if not all_segments_data:
        print("No segments were transcribed from any audio files.")
        return

    df = pd.DataFrame(all_segments_data)
    df = df[["Audio Filename", "Start Time (s)", "End Time (s)", "Is Flagged", "Flag Reason", "Transcription", "Detected Language", "Confidence Score"]]

    try:
        df.to_excel(output_excel_path, index=False, engine='openpyxl')
        print(f"\n✅ Successfully saved all segments to '{output_excel_path}'")
    except Exception as e:
        print(f"\nError saving Excel file: {e}")

if __name__ == '__main__':
    # --- Configuration ---
    # IMPORTANT: Update these paths before running the script
    INPUT_AUDIO_FOLDER = "path/to/your/audio_files"
    OUTPUT_EXCEL_FILE = "path/to/save/your/output.xlsx"
    OUTPUT_CROPPED_FOLDER = "path/to/your/cropped_audio" # Folder for saving flagged clips

    # You can adjust the confidence threshold here
    CONFIDENCE_THRESHOLD = 0.7

    # --- Run the main function ---
    process_and_flag_audios(INPUT_AUDIO_FOLDER, OUTPUT_EXCEL_FILE, OUTPUT_CROPPED_FOLDER, CONFIDENCE_THRESHOLD)