import pandas as pd
import os
import json

# File paths
audio_dir = r"D:\Data set\Project\audio"
json_dir = r"D:\Data set\Project\json"
excel_file = r"D:\Data set\Project\annotations.xlsx"
output_dirs = {
    "segments": r"D:\Data set\Project\segments",
    "augmented": r"D:\Data set\Project\augmented",
    "features": r"D:\Data set\Project\features"
}

# Create output directories
for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# Load Excel file
try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    print(f"Error: {excel_file} not found. Run create_excel_from_json.py to generate it.")
    exit()
except ImportError as e:
    print(f"Error: Failed to load Excel due to missing dependency: {e}")
    print("Run: pip install openpyxl")
    exit()
except Exception as e:
    print(f"Error loading Excel: {e}")
    exit()

# Verify Excel columns (adjust these if your column names differ)
expected_columns = ["Clip ID", "Record Annotation", "Event Start (ms)", "Event End (ms)", "Event Type"]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Excel missing columns: {missing_columns}")
    print("Current columns:", list(df.columns))
    print("Please rename columns in annotations.xlsx to match:", expected_columns)
    print("Or update expected_columns in this script.")
    exit()

# Verify audio and JSON files
try:
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]
    json_files = [f for f in os.listdir(json_dir) if f.endswith(".json")]
except FileNotFoundError as e:
    print(f"Error: Directory not found: {e}")
    exit()

if len(audio_files) != 1655:
    print(f"Warning: Found {len(audio_files)} audio files in {audio_dir}, expected 1655")
if len(json_files) != 1655:
    print(f"Warning: Found {len(json_files)} JSON files in {json_dir}, expected 1655")

# Verify Excel has all clips
clip_ids = df["Clip ID"].unique()
if len(clip_ids) != 1655:
    print(f"Warning: Excel has {len(clip_ids)} unique clips, expected 1655")

# Function to load JSON if Excel is incomplete
def load_json(clip_id):
    json_path = os.path.join(json_dir, clip_id.replace(".wav", ".json"))
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found")
        return None

# Use double backslashes to avoid syntax warning
print("Step 1: Data preparation complete. Output folders created in D:\\Data set\\Project.")
print(f"Audio files: {len(audio_files)}, JSON files: {len(json_files)}, Clips in Excel: {len(clip_ids)}")