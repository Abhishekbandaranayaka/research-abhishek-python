import numpy as np
import librosa
import joblib

# File paths
model_file = r"D:\Data set\Project\trained_model.pkl"
label_classes_file = r"D:\Data set\Project\label_classes.npy"
new_audio_file = r"D:\Data set\Project\audio\66239166_9.6_1_p3_4339.wav"  # Replace with your new audio file

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

# Extract features from the new audio file
features = extract_features(new_audio_file)
if features is None:
    exit()

# Reshape features for prediction (model expects shape: 1×16)
features = features.reshape(1, -1)

# Make prediction
try:
    prediction = model.predict(features)
    predicted_class = label_classes[prediction[0]]
    print(f"Prediction for {new_audio_file}:")
    print(f"Predicted class index: {prediction[0]}")
    print(f"Predicted Event Label: {predicted_class}")
except Exception as e:
    print(f"Error making prediction: {e}")
    exit()

print("Step 6: Prediction complete.")