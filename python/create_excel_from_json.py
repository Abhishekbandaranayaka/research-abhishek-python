import pandas as pd
import os
import json

# File paths
json_dir = r"D:\Data set\Project\json"
excel_file = r"D:\Data set\Project\annotations.xlsx"

# Initialize list for Excel rows
rows = []

# Process each JSON file
json_files = [f for f in os.listdir(json_dir) if f.endswith(".json")]
for json_file in json_files:
    json_path = os.path.join(json_dir, json_file)
    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        clip_id = json_file.replace(".json", ".wav")
        record_annotation = data.get("record_annotation", "Unknown")
        event_annotations = data.get("event_annotation", [])

        # Add each event as a row
        for event in event_annotations:
            rows.append({
                "Clip ID": clip_id,
                "Record Annotation": record_annotation,
                "Event Start (ms)": event.get("start", 0),
                "Event End (ms)": event.get("end", 0),
                "Event Type": event.get("type", "No Event")
            })

        # If no events, add a row for the clip
        if not event_annotations:
            rows.append({
                "Clip ID": clip_id,
                "Record Annotation": record_annotation,
                "Event Start (ms)": 0,
                "Event End (ms)": 0,
                "Event Type": "No Event"
            })
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

# Create Excel
df = pd.DataFrame(rows)
df.to_excel(excel_file, index=False)

print(f"Excel file created: {excel_file}, Rows: {len(df)}")