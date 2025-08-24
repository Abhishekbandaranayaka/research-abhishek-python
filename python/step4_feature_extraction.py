import pandas as pd
import numpy as np
import os
import librosa
import soundfile as sf
from sklearn.preprocessing import LabelEncoder

# File paths
segments_dir = r"D:\Data set\Project\segments"
augmented_dir = r"D:\Data set\Project\augmented"
excel_file = r"D:\Data set\Project\updated_annotations.xlsx"
features_file = r"D:\Data set\Project\features.npy"
labels_file = r"D:\Data set\Project\labels.npy"


# Function to extract features from an audio file
def extract_features(file_path, sr=22050, n_mfcc=13):
    try:
        # Load audio
        audio, sr = librosa.load(file_path, sr=sr)

        # Extract features
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)  # Mean of MFCCs over time

        # Additional features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=audio))

        # Combine features into a single array
        features = np.concatenate([
            mfccs_mean,
            [spectral_centroid, spectral_rolloff, zero_crossing_rate]
        ])
        return features
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None


# Load Excel
try:
    df = pd.read_excel(excel_file)
    print(f"Loaded Excel with {len(df)} rows")
except FileNotFoundError:
    print(f"Error: {excel_file} not found. Ensure Step 3 completed successfully.")
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

# Initialize lists for features and labels
all_features = []
all_labels = []
label_encoder = LabelEncoder()

# Process each segment (original and augmented)
for idx, row in df.iterrows():
    segment_id = row["Segment ID"]
    augmentation_type = row["Augmentation Type"]
    event_label = row["Event Label"]

    # Determine file path based on augmentation type
    if str(augmentation_type).lower() in ["none", "nan"]:
        file_path = os.path.join(segments_dir, f"{segment_id}.wav")
    else:
        file_path = os.path.join(augmented_dir, f"{segment_id}.wav")

    # Extract features
    features = extract_features(file_path)
    if features is not None:
        all_features.append(features)
        all_labels.append(event_label)
    else:
        print(f"Skipping {segment_id} due to feature extraction failure")

# Convert to NumPy arrays
features_array = np.array(all_features)
labels_array = label_encoder.fit_transform(all_labels)

# Save features and labels
try:
    np.save(features_file, features_array)
    np.save(labels_file, labels_array)
    print(f"Features shape: {features_array.shape}")
    print(f"Labels shape: {labels_array.shape}")
    print(f"Saved features to {features_file}")
    print(f"Saved labels to {labels_file}")
except Exception as e:
    print(f"Error saving features/labels: {e}")
    exit()

# Save label encoder classes for later use
np.save(r"D:\Data set\Project\label_classes.npy", label_encoder.classes_)
print(f"Saved label classes to D:\Data set\Project\label_classes.npy")
print("Step 4: Feature Extraction complete.")