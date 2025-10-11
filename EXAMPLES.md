# 📖 Usage Examples

Practical examples for using the Audio Language Compliance Checker.

---

## 🎯 Example 1: Call Center Quality Assurance

### Scenario
You manage a call center where agents should only speak English and Hindi. You want to flag any calls where other languages are used.

### Setup

1. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

2. **Configure (Sidebar):**
   - **Authorized Languages:** English (en), Hindi (hi)
   - **Model Size:** large-v3-turbo
   - **Confidence Threshold:** 0.7

3. **Input (Tab 1):**
   - **Audio Folder:** `C:/CallRecordings/2024-01`
   - Click "🔍 Scan Folder"
   - Select all files or specific calls

4. **Process (Tab 3):**
   - Click "🚀 Start Processing"
   - Wait for completion

5. **Review Results:**
   - Filter for "Flagged only"
   - Check segments with "Language mismatch"
   - Listen to flagged clips in `cropped_audio/`

### Expected Output

```
output.xlsx:
- 150 total segments
- 12 flagged (8%)
- Reasons: 8 Spanish, 3 French, 1 Low confidence

cropped_audio/:
- call_001_merged_1_5000ms_to_12000ms.wav
- call_045_merged_1_23000ms_to_28000ms.wav
- ...
```

---

## 🎯 Example 2: Podcast Content Moderation

### Scenario
You produce English-only podcasts and want to ensure no unauthorized language segments slip through.

### Setup

1. **Configure:**
   - **Authorized Languages:** English (en) only
   - **Model Size:** large-v3-turbo
   - **Confidence Threshold:** 0.8 (stricter)
   - **Merge Flagged Segments:** True
   - **Max Merge Gap:** 2000ms (longer context)

2. **Input:**
   - **Audio Folder:** `D:/Podcasts/Episodes/Season2`

3. **Parameters (Tab 2):**
   - **Min Silence Length:** 700ms (longer pauses in podcasts)
   - **Silence Threshold:** -35 dBFS (less strict for music)
   - **Min Segment Length:** 2000ms (longer segments)

4. **Process and Review:**
   - Check for any non-English segments
   - Review low-confidence segments for audio quality issues

---

## 🎯 Example 3: Multilingual Customer Support

### Scenario
Your support team handles English, Spanish, and French. You want to flag any other languages and low-quality audio.

### Setup

1. **Configure:**
   - **Authorized Languages:** English (en), Spanish (es), French (fr)
   - **Model Size:** large-v3-turbo
   - **Confidence Threshold:** 0.6 (more lenient)

2. **Input:**
   - **Audio Folder:** `E:/Support/Recordings/Week_42`

3. **Advanced Settings:**
   - **Merge Flagged Segments:** True
   - **Enable Logging:** True (for audit trail)

4. **Review:**
   - Filter by language to see distribution
   - Check flagged segments for quality issues
   - Export report for management

---

## 🎯 Example 4: Educational Content Verification

### Scenario
You're creating language learning materials and need to verify that each audio file contains only the target language.

### Setup

1. **For English lessons:**
   - **Authorized Languages:** English (en) only
   - **Confidence Threshold:** 0.9 (very strict)

2. **For Spanish lessons:**
   - **Authorized Languages:** Spanish (es) only
   - **Confidence Threshold:** 0.9

3. **Batch Processing:**
   - Process English folder
   - Change authorized language to Spanish
   - Process Spanish folder
   - Compare results

---

## 🎯 Example 5: Legal Compliance Monitoring

### Scenario
Monitor recorded conversations for compliance, flagging any segments that might need review.

### Setup

1. **Configure:**
   - **Authorized Languages:** English (en), Hindi (hi)
   - **Model Size:** large-v3 (most accurate)
   - **Confidence Threshold:** 0.75
   - **Enable Logging:** True (required for audit)

2. **Parameters:**
   - **Min Silence Length:** 300ms (catch short utterances)
   - **Silence Threshold:** -45 dBFS (strict detection)
   - **Min Segment Length:** 500ms (short segments)

3. **Output:**
   - **Excel Path:** `Compliance_Report_2024-01.xlsx`
   - **Cropped Folder:** `Compliance_Flagged_Audio/2024-01`

4. **Review Process:**
   - Legal team reviews all flagged segments
   - Low confidence segments checked for clarity
   - All results archived for compliance

---

## 🎯 Example 6: Fast Batch Processing

### Scenario
You have 1000+ audio files and need fast processing.

### Optimization Strategy

1. **Use Smaller Model:**
   - **Model Size:** base or small
   - Trade accuracy for speed

2. **Adjust Parameters:**
   - **Min Segment Length:** 2000ms (fewer segments)
   - **Merge Flagged Segments:** True (fewer output files)

3. **Hardware:**
   - Use GPU if available (5-10x faster)
   - Close other applications

4. **Batch Strategy:**
   - Process 100 files at a time
   - Monitor memory usage
   - Save results incrementally

---

## 🎯 Example 7: High-Accuracy Transcription

### Scenario
You need the most accurate transcription possible, speed is not a concern.

### Setup

1. **Configure:**
   - **Model Size:** large-v3 (most accurate)
   - **Confidence Threshold:** 0.9 (very strict)

2. **Audio Preparation:**
   - Use high-quality WAV or FLAC files
   - Ensure minimal background noise
   - Normalize audio levels

3. **Parameters:**
   - **Min Silence Length:** 400ms (precise segmentation)
   - **Silence Threshold:** -42 dBFS (balanced)
   - **Min Segment Length:** 800ms

4. **Review:**
   - Manually verify all flagged segments
   - Check transcription accuracy
   - Adjust parameters if needed

---

## 🎯 Example 8: Testing and Calibration

### Scenario
First-time setup, testing with sample files to find optimal parameters.

### Process

1. **Start Small:**
   - Use 5-10 sample files
   - **Model Size:** base (fast testing)

2. **Test Different Thresholds:**
   
   **Test 1: Lenient**
   - Confidence: 0.5
   - Review: How many false positives?
   
   **Test 2: Moderate**
   - Confidence: 0.7
   - Review: Good balance?
   
   **Test 3: Strict**
   - Confidence: 0.9
   - Review: Missing any issues?

3. **Test VAD Parameters:**
   
   **For noisy audio:**
   - Silence Threshold: -35 dBFS
   
   **For clean audio:**
   - Silence Threshold: -45 dBFS
   
   **For speech with pauses:**
   - Min Silence Length: 700ms

4. **Find Optimal Settings:**
   - Document what works best
   - Save configuration
   - Use for production

---

## 🎯 Example 9: Integration with Workflow

### Scenario
Integrate the tool into your existing audio processing pipeline.

### Python Script Example

```python
from main import process_and_flag_audios
import os
from datetime import datetime

# Configuration
INPUT_FOLDERS = [
    'recordings/team_a',
    'recordings/team_b',
    'recordings/team_c'
]

AUTHORIZED_LANGS = ['en', 'hi']
MODEL_SIZE = 'large-v3-turbo'

# Process each folder
for folder in INPUT_FOLDERS:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    team_name = os.path.basename(folder)
    
    print(f"Processing {team_name}...")
    
    result = process_and_flag_audios(
        input_folder=folder,
        output_excel_path=f"reports/{team_name}_{timestamp}.xlsx",
        output_cropped_folder=f"flagged/{team_name}_{timestamp}",
        confidence_threshold=0.7,
        authorized_languages=AUTHORIZED_LANGS,
        model_size=MODEL_SIZE,
        enable_logging=True,
        log_folder=f"logs/{team_name}"
    )
    
    if result['success']:
        stats = result['stats']
        print(f"✅ {team_name}: {stats['flagged_segments']} flagged")
    else:
        print(f"❌ {team_name}: Failed - {result['error']}")

print("All folders processed!")
```

---

## 🎯 Example 10: Custom Language Combinations

### Scenario
Different projects require different language combinations.

### Project A: US-India Team
```
Authorized: English (en), Hindi (hi)
Threshold: 0.7
```

### Project B: European Support
```
Authorized: English (en), French (fr), German (de), Spanish (es)
Threshold: 0.65
```

### Project C: Asian Markets
```
Authorized: English (en), Japanese (ja), Korean (ko), Chinese (zh)
Threshold: 0.7
```

### Implementation

1. **Save Configurations:**
   - Create `config_project_a.json`
   - Create `config_project_b.json`
   - Create `config_project_c.json`

2. **Load Configuration:**
   - In Streamlit, manually set parameters
   - Click "💾 Save Configuration"
   - Rename `config.json` to project-specific name

3. **Switch Between Projects:**
   - Copy appropriate config to `config.json`
   - Restart Streamlit app
   - Settings auto-load

---

## 💡 Tips from Examples

### For Best Results:
1. **Start with defaults** - Adjust based on results
2. **Test on samples** - Before processing large batches
3. **Use appropriate model** - Balance speed vs accuracy
4. **Monitor first run** - Check logs for issues
5. **Iterate parameters** - Fine-tune for your use case

### Common Patterns:
- **High accuracy needed** → large-v3, threshold 0.9
- **Fast processing needed** → base/small, threshold 0.6
- **Balanced approach** → large-v3-turbo, threshold 0.7
- **Noisy audio** → Adjust silence threshold to -35
- **Clean audio** → Adjust silence threshold to -45

---

## 📊 Results Interpretation

### Flagged Percentage Guidelines:

- **< 5%** - Normal, good quality audio
- **5-15%** - Moderate issues, review flagged segments
- **15-30%** - Significant issues, check parameters
- **> 30%** - Major issues, verify:
  - Correct authorized languages selected
  - Appropriate confidence threshold
  - Audio quality is acceptable
  - Model size is adequate

---

## 🆘 Troubleshooting Examples

### "Too many segments flagged"
**Solution:** Lower confidence threshold from 0.7 to 0.5

### "Missing obvious issues"
**Solution:** Raise confidence threshold from 0.7 to 0.9

### "Processing too slow"
**Solution:** Use smaller model (base instead of large-v3)

### "Segments split incorrectly"
**Solution:** Adjust min_silence_len (increase for longer pauses)

### "Background noise causing issues"
**Solution:** Increase silence_thresh from -40 to -35

---

**Need more help?** Check the full documentation in `README_STREAMLIT.md`
