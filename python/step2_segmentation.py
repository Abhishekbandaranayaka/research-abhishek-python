import pandas as pd
import os
import librosa
import soundfile as sf
import numpy as np

# File paths
audio_dir = r"D:\Data set\Project\audio"
excel_file = r"D:\Data set\Project\annotations.xlsx"
segments_dir = r"D:\Data set\Project\segments"
output_excel = r"D:\Data set\Project\updated_annotations.xlsx"

# Parameters
segment_length = 2  # Seconds
overlap = 0.5  # 50% overlap
sr = 22050  # Sample rate (adjust if your audio differs)
samples_per_segment = int(segment_length * sr)
step_size = int(samples_per_segment * (1 - overlap))

# Load Excel
try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    print(f"Error: {excel_file} not found. Ensure annotations.xlsx exists.")
    exit()
except Exception as e:
    print(f"Error loading Excel: {e}")
    exit()

# Verify Excel columns
expected_columns = ["Clip ID", "Record Annotation", "Event Start (ms)", "Event End (ms)", "Event Type"]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Excel missing columns: {missing_columns}")
    print("Current columns:", list(df.columns))
    print("Please rename columns in annotations.xlsx to match:", expected_columns)
    exit()

# Initialize list for new Excel rows
new_rows = []

# Process each clip
clip_ids = df["Clip ID"].unique()
print(f"Processing {len(clip_ids)} clips...")
for clip_id in clip_ids:
    # Load audio
    audio_path = os.path.join(audio_dir, clip_id)
    try:
        audio, _ = librosa.load(audio_path, sr=sr)
    except Exception as e:
        print(f"Error loading {audio_path}: {e}")
        continue

    # Get event annotations from Excel
    clip_events = df[df["Clip ID"] == clip_id][
        ["Event Start (ms)", "Event End (ms)", "Event Type", "Record Annotation"]]

    # Segment audio
    for start_sample in range(0, len(audio) - samples_per_segment + 1, step_size):
        end_sample = start_sample + samples_per_segment
        segment = audio[start_sample:end_sample]

        # Calculate segment time
        start_time_s = start_sample / sr
        end_time_s = end_sample / sr
        start_time_ms = start_time_s * 1000
        end_time_ms = end_time_s * 1000

        # Generate segment ID
        segment_id = f"{clip_id.split('.')[0]}_seg_{int(start_time_s)}"

        # Label segment based on event overlap
        event_label = "No Event"
        for _, event in clip_events.iterrows():
            event_start_ms = event["Event Start (ms)"]
            event_end_ms = event["Event End (ms)"]
            if not (end_time_ms < event_start_ms or start_time_ms > event_end_ms):
                event_label = event["Event Type"]
                break

        # Save segment
        segment_path = os.path.join(segments_dir, f"{segment_id}.wav")
        try:
            sf.write(segment_path, segment, sr)
        except Exception as e:
            print(f"Error saving {segment_path}: {e}")
            continue

        # Add to Excel rows
        new_rows.append({
            "Clip ID": clip_id,
            "Segment ID": segment_id,
            "Start Time (s)": start_time_s,
            "End Time (s)": end_time_s,
            "Augmentation Type": "None",
            "Event Label": event_label,
            "Clip Label": clip_events["Record Annotation"].iloc[0] if not clip_events.empty else "Unknown"
        })

# Create new Excel with segments
segment_df = pd.DataFrame(new_rows)
segment_df.to_excel(output_excel, index=False)

print(f"Step 2: Segmentation complete. {len(segment_df)} segments saved in {segments_dir}")
print(f"Excel updated: {output_excel}")