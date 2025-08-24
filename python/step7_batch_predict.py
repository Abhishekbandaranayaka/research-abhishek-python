import numpy as np
import librosa
import joblib
import os
import pandas as pd

# File paths
model_file = r"D:\Data set\Project\trained_model.pkl"
label_classes_file = r"D:\Data set\Project\label_classes.npy"
new_audio_dir = r"D:\Data set\Project\audio"  # Directory with new audio files
output_csv = r"D:\Data set\Project\predictions.csv"


# Function to extract features (same as Step 4)
def extract_features(file_path, sr=22050, n_mfcc=13):
    try:
        audio, sr = librosa.load(file_path, sr=sr)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=audio))
        features = np.concatenate([
            mfccs_mean,
            [spectral_centroid, spectral_rolloff, zero_crossing_rate]
        ])
        return features
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None


# Load the trained model and label classes
try:
    model = joblib.load(model_file)
    label_classes = np.load(label_classes_file)
    print("Loaded model and label classes.")
    print("Label classes:", label_classes)
except FileNotFoundError as e:
    print(f"Error: {e}. Ensure Step 5 completed successfully.")
    exit()
except Exception as e:
    print(f"Error loading model/labels: {e}")
    exit()

# Get list of new audio files
audio_files = [f for f in os.listdir(new_audio_dir) if f.endswith(".wav")]
print(f"Found {len(audio_files)} audio files to process.")

# Initialize lists for predictions
results = []

# Process each audio file
for audio_file in audio_files:
    file_path = os.path.join(new_audio_dir, audio_file)

    # Extract features
    features = extract_features(file_path)
    if features is None:
        print(f"Skipping {audio_file} due to feature extraction failure")
        continue

    # Reshape features for prediction
    features = features.reshape(1, -1)

    # Make prediction
    try:
        prediction = model.predict(features)
        predicted_class = label_classes[prediction[0]]
        print(f"Prediction for {audio_file}: {predicted_class}")

        # Store result
        results.append({
            "Audio File": audio_file,
            "Predicted Class Index": prediction[0],
            "Predicted Event Label": predicted_class
        })
    except Exception as e:
        print(f"Error predicting for {audio_file}: {e}")
        continue

# Save predictions to CSV
if results:
    df_results = pd.DataFrame(results)
    try:
        df_results.to_csv(output_csv, index=False)
        print(f"Saved predictions to {output_csv}")
    except Exception as e:
        print(f"Error saving predictions: {e}")
        exit()
else:
    print("No predictions were made.")

print("Step 7: Batch Prediction complete.")