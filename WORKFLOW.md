# 🔄 Workflow Diagram

Visual representation of the Audio Language Compliance Checker workflow.

---

## 📊 High-Level Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                          │
│                   (Streamlit Web UI)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  CONFIGURATION PHASE                         │
│  • Select Whisper Model (tiny → large-v3-turbo)            │
│  • Choose Authorized Languages (en, hi, es, etc.)          │
│  • Set Confidence Threshold (0.0 - 1.0)                    │
│  • Configure VAD Parameters                                 │
│  • Specify Input/Output Paths                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FILE SELECTION PHASE                       │
│  • Scan Audio Folder                                        │
│  • Display Available Files (with metadata)                  │
│  • User Selects Files to Process                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING PHASE                           │
│                  (Backend: main.py)                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────┐                  ┌──────────────────┐
│  Load Whisper    │                  │  Setup Logging   │
│     Model        │                  │   & Progress     │
└──────────────────┘                  └──────────────────┘
        │                                       │
        └───────────────────┬───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              FOR EACH AUDIO FILE                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Voice Activity Detection (VAD)                     │
│  • Load audio file                                          │
│  • Detect non-silent segments                               │
│  • Filter by minimum segment length                         │
│  • Output: List of (start_ms, end_ms) tuples               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Segment Transcription                              │
│  FOR EACH SPEECH SEGMENT:                                   │
│    • Extract audio segment                                  │
│    • Save temporary WAV file                                │
│    • Transcribe with Whisper                                │
│    • Get: text, language, confidence                        │
│    • Clean up temporary file                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Flagging Logic                                     │
│  FOR EACH TRANSCRIBED SEGMENT:                              │
│    ┌─────────────────────────────────────┐                 │
│    │ Is language in authorized list?     │                 │
│    └─────────────────────────────────────┘                 │
│              │                    │                         │
│             YES                  NO                         │
│              │                    │                         │
│              ▼                    ▼                         │
│    ┌──────────────────┐  ┌──────────────────┐             │
│    │ Check Confidence │  │ FLAG: Language   │             │
│    │    Score         │  │    Mismatch      │             │
│    └──────────────────┘  └──────────────────┘             │
│              │                                              │
│    ┌─────────┴─────────┐                                   │
│    │                   │                                   │
│   ≥ Threshold    < Threshold                               │
│    │                   │                                   │
│    ▼                   ▼                                   │
│  ┌──────┐      ┌──────────────────┐                       │
│  │ PASS │      │ FLAG: Low        │                       │
│  └──────┘      │   Confidence     │                       │
│                └──────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Segment Merging (if enabled)                       │
│  • Identify consecutive flagged segments                    │
│  • Merge if gap ≤ max_merge_gap_ms                         │
│  • Create merged audio clips                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Export Results                                     │
│  • Save flagged/merged audio clips (WAV)                    │
│  • Collect all segment data                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              END OF FILE LOOP                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Generate Excel Report                              │
│  • Compile all segments from all files                      │
│  • Create DataFrame with columns:                           │
│    - Audio Filename                                         │
│    - Start Time (s) / End Time (s)                         │
│    - Is Flagged / Flag Reason                              │
│    - Transcription                                          │
│    - Detected Language                                      │
│    - Confidence Score                                       │
│  • Export to Excel (.xlsx)                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: Return Results to Streamlit                        │
│  • Processing statistics                                    │
│  • Output file paths                                        │
│  • Success/error status                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  RESULTS DISPLAY PHASE                       │
│                   (Streamlit Web UI)                         │
│  • Show processing summary                                  │
│  • Display statistics (files, segments, flags)              │
│  • Preview Excel results (first 20 rows)                    │
│  • Provide download button                                  │
│  • Show output file paths                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER REVIEW                               │
│  • Download Excel report                                    │
│  • Listen to flagged audio clips                           │
│  • Filter results by language/confidence                    │
│  • Take corrective action                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Decision Tree: Segment Flagging

```
                    ┌─────────────────────┐
                    │  Transcribed        │
                    │  Segment            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Language in          │
                    │ Authorized List?     │
                    └──────────────────────┘
                         │            │
                        YES          NO
                         │            │
                         ▼            ▼
              ┌──────────────┐  ┌──────────────┐
              │ Confidence   │  │   FLAG:      │
              │ ≥ Threshold? │  │  Language    │
              └──────────────┘  │  Mismatch    │
                   │      │     └──────────────┘
                  YES    NO            │
                   │      │            │
                   ▼      ▼            │
              ┌──────┐ ┌──────────┐   │
              │ PASS │ │  FLAG:   │   │
              │      │ │   Low    │   │
              │      │ │Confidence│   │
              └──────┘ └──────────┘   │
                   │         │        │
                   └─────────┴────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Add to Results  │
                    │ DataFrame       │
                    └─────────────────┘
```

---

## 📁 Data Flow Diagram

```
┌──────────────┐
│ Audio Files  │
│  (.mp3, .wav)│
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  PyDub (pydub)       │
│  • Load audio        │
│  • VAD detection     │
│  • Segment extraction│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Whisper Model       │
│  • Transcription     │
│  • Language detect   │
│  • Confidence score  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Flagging Logic      │
│  • Language check    │
│  • Confidence check  │
│  • Reason assignment │
└──────┬───────────────┘
       │
       ├─────────────────────┐
       │                     │
       ▼                     ▼
┌──────────────┐    ┌─────────────────┐
│ Excel Report │    │ Flagged Audio   │
│  (.xlsx)     │    │ Clips (.wav)    │
└──────────────┘    └─────────────────┘
       │                     │
       └──────────┬──────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Streamlit UI    │
         │ • Preview       │
         │ • Download      │
         │ • Filter        │
         └─────────────────┘
```

---

## 🔄 State Diagram: Processing States

```
┌─────────┐
│  IDLE   │ ◄──────────────────────┐
└────┬────┘                        │
     │                             │
     │ User clicks                 │
     │ "Start Processing"          │
     │                             │
     ▼                             │
┌──────────────┐                   │
│ VALIDATING   │                   │
│ • Check paths│                   │
│ • Check langs│                   │
└────┬─────────┘                   │
     │                             │
     │ Validation OK               │
     │                             │
     ▼                             │
┌──────────────┐                   │
│ LOADING      │                   │
│ • Load model │                   │
│ • Setup logs │                   │
└────┬─────────┘                   │
     │                             │
     │ Model loaded                │
     │                             │
     ▼                             │
┌──────────────┐                   │
│ PROCESSING   │                   │
│ • VAD        │                   │
│ • Transcribe │                   │
│ • Flag       │                   │
│ • Merge      │                   │
└────┬─────────┘                   │
     │                             │
     │ All files done              │
     │                             │
     ▼                             │
┌──────────────┐                   │
│ EXPORTING    │                   │
│ • Save Excel │                   │
│ • Save audio │                   │
└────┬─────────┘                   │
     │                             │
     │ Export complete             │
     │                             │
     ▼                             │
┌──────────────┐                   │
│ COMPLETE     │                   │
│ • Show stats │                   │
│ • Show paths │                   │
└────┬─────────┘                   │
     │                             │
     │ User reviews                │
     │ or starts new               │
     │                             │
     └─────────────────────────────┘

     ERROR at any stage
          │
          ▼
     ┌─────────┐
     │  ERROR  │
     │ • Show  │
     │ message │
     └─────────┘
```

---

## 🎨 UI Component Hierarchy

```
Streamlit App (app.py)
│
├── Sidebar
│   ├── Navigation
│   │   ├── 📘 Tool & Usage Guide
│   │   └── 🚀 Main Processing
│   │
│   ├── Configuration (Main Processing only)
│   │   ├── Whisper Model
│   │   │   ├── Model Path (text input)
│   │   │   └── Model Size (dropdown)
│   │   │
│   │   ├── Device Info (display)
│   │   │
│   │   └── Authorized Languages
│   │       └── Multi-select dropdown
│   │
│   └── About Section
│       └── Version info
│
└── Main Content Area
    │
    ├── Page 1: Tool & Usage Guide
    │   ├── Title & Description
    │   ├── Purpose Section
    │   ├── How It Works Section
    │   ├── Key Concepts Section
    │   ├── Output Files Section
    │   └── Tips Section
    │
    └── Page 2: Main Processing
        │
        ├── Tab 1: Input Files
        │   ├── Folder Path Input
        │   ├── Scan Button
        │   ├── Files Table
        │   └── File Selection
        │
        ├── Tab 2: Parameters
        │   ├── Detection Parameters
        │   │   ├── Confidence Threshold (slider)
        │   │   ├── Min Silence Length (number)
        │   │   ├── Silence Threshold (number)
        │   │   └── Min Segment Length (number)
        │   │
        │   ├── Merging Parameters
        │   │   ├── Merge Toggle
        │   │   └── Max Merge Gap (number)
        │   │
        │   ├── Logging
        │   │   ├── Enable Logging (toggle)
        │   │   └── Log Folder (text)
        │   │
        │   ├── Output Paths
        │   │   ├── Excel Path (text)
        │   │   └── Cropped Folder (text)
        │   │
        │   └── Save Config Button
        │
        └── Tab 3: Process & Results
            ├── Validation Messages
            ├── Start Processing Button
            ├── Processing Status
            │   ├── Progress Bar
            │   ├── Status Text
            │   └── Log Expander
            │
            └── Results Display
                ├── Summary Statistics
                ├── Output Paths
                ├── Results Preview
                │   ├── Filters
                │   └── Data Table
                └── Download Button
```

---

## 🔧 Configuration Flow

```
┌─────────────────┐
│ User Opens App  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Load config.json    │
│ (if exists)         │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Populate UI         │
│ with saved values   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ User Modifies       │
│ Settings            │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ User Clicks         │
│ "Save Config"       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Write to            │
│ config.json         │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Show Success        │
│ Message             │
└─────────────────────┘
```

---

## 📊 Processing Timeline

```
Time →

0s     ┌──────────────────────────────────────────┐
       │ Initialize                                │
       │ • Load config                            │
       │ • Setup UI                               │
       └──────────────────────────────────────────┘

1s     ┌──────────────────────────────────────────┐
       │ User Configuration                        │
       │ • Select languages                       │
       │ • Set parameters                         │
       │ • Choose files                           │
       └──────────────────────────────────────────┘

2s     ┌──────────────────────────────────────────┐
       │ Start Processing                          │
       │ • Validate inputs                        │
       │ • Load Whisper model (first time: 30s+) │
       └──────────────────────────────────────────┘

30s+   ┌──────────────────────────────────────────┐
       │ Process Files                             │
       │ • File 1: VAD → Transcribe → Flag        │
       │ • File 2: VAD → Transcribe → Flag        │
       │ • ...                                    │
       │ (Time varies: 1-10 min per file)         │
       └──────────────────────────────────────────┘

Varies ┌──────────────────────────────────────────┐
       │ Export Results                            │
       │ • Generate Excel                         │
       │ • Save audio clips                       │
       └──────────────────────────────────────────┘

+5s    ┌──────────────────────────────────────────┐
       │ Display Results                           │
       │ • Show statistics                        │
       │ • Preview data                           │
       │ • Enable download                        │
       └──────────────────────────────────────────┘
```

---

## 🎯 Use Case Flow: Call Center QA

```
1. QA Manager Opens App
   └─→ Streamlit launches in browser

2. Configure for Call Center
   ├─→ Authorized Languages: English, Hindi
   ├─→ Confidence Threshold: 0.7
   └─→ Model: large-v3-turbo

3. Select Call Recordings
   ├─→ Input Folder: "C:/Calls/Week_42"
   ├─→ Scan: 150 files found
   └─→ Select: All files

4. Start Processing
   ├─→ Progress: 0/150 files
   ├─→ Processing: File 1, 2, 3...
   └─→ Complete: 150/150 files

5. Review Results
   ├─→ Total Segments: 2,340
   ├─→ Flagged: 187 (8%)
   ├─→ Reasons:
   │   ├─→ 120 Spanish
   │   ├─→ 45 French
   │   └─→ 22 Low confidence
   └─→ Download Excel report

6. Manual Review
   ├─→ Listen to flagged clips
   ├─→ Verify language violations
   └─→ Take corrective action

7. Generate Report
   └─→ Share Excel with management
```

---

This workflow documentation provides a comprehensive visual guide to understanding how the Audio Language Compliance Checker operates from start to finish.
