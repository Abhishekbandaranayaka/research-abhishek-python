import pandas as pd
import os
import librosa
import soundfile as sf
from audiomentations import Compose, AddGaussianNoise, Gain

# File paths
segments_dir = r"D:\Data set\Project\segments"
augmented_dir = r"D:\Data set\Project\augmented"
excel_file = r"D:\Data set\Project\updated_annotations.xlsx"
output_excel = r"D:\Data set\Project\updated_annotations.xlsx"

# Define augmentations
augment_noise = AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=1.0)
augment_gain = Gain(min_gain_db=-12, max_gain_db=12, p=1.0)

# Load Excel
try:
    df = pd.read_excel(excel_file)
    print(f"Loaded Excel with {len(df)} rows")
    print("Columns:", list(df.columns))
except FileNotFoundError:
    print(f"Error: {excel_file} not found. Ensure Step 2 completed successfully.")
    exit()
except Exception as e:
    print(f"Error loading Excel: {e}")
    exit()

# Verify Excel columns
expected_columns = ["Clip ID", "Segment ID", "Start Time (s)", "End Time (s)", "Augmentation Type", "Event Label",
                    "Clip Label"]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Excel missing columns: {missing_columns}")
    print("Current columns:", list(df.columns))
    exit()

# Handle NaN and normalize Augmentation Type
df["Augmentation Type"] = df["Augmentation Type"].fillna("none").astype(str).str.strip().str.lower()
print("Augmentation Type values (after normalization):", df["Augmentation Type"].unique())

# Process only original segments (Augmentation Type == "none")
segments = df[df["Augmentation Type"] == "none"]
print(f"Augmenting {len(segments)} original segments...")

# Initialize list for new Excel rows
new_rows = []

# Process each segment
for _, row in segments.iterrows():
    segment_id = row["Segment ID"]
    segment_path = os.path.join(segments_dir, f"{segment_id}.wav")

    # Load segment
    try:
        audio, sr = librosa.load(segment_path, sr=22050)
    except Exception as e:
        print(f"Error loading {segment_path}: {e}")
        continue

    # Apply augmentations
    for aug_type, aug in [("Noise", augment_noise), ("Gain", augment_gain)]:
        try:
            augmented_audio = aug(samples=audio, sample_rate=sr)

            # Save augmented segment
            aug_segment_id = f"{segment_id}_{aug_type.lower()}"
            aug_segment_path = os.path.join(augmented_dir, f"{aug_segment_id}.wav")
            sf.write(aug_segment_path, augmented_audio, sr)

            # Add to Excel rows
            new_rows.append({
                "Clip ID": row["Clip ID"],
                "Segment ID": aug_segment_id,
                "Start Time (s)": row["Start Time (s)"],
                "End Time (s)": row["End Time (s)"],
                "Augmentation Type": aug_type,
                "Event Label": row["Event Label"],
                "Clip Label": row["Clip Label"]
            })
        except Exception as e:
            print(f"Error processing {segment_id} for {aug_type}: {e}")
            continue

# Update Excel
aug_df = pd.DataFrame(new_rows)
if not aug_df.empty:
    updated_df = pd.concat([df, aug_df], ignore_index=True)
    try:
        updated_df.to_excel(output_excel, index=False)
    except Exception as e:
        print(f"Error saving Excel: {e}")
        exit()
else:
    print("Warning: No augmented segments were created.")

print(f"Step 3: Augmentation complete. {len(aug_df)} augmented segments saved in {augmented_dir}")
print(f"Excel updated: {output_excel}")