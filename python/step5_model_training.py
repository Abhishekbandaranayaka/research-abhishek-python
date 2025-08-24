import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# File paths
features_file = r"D:\Data set\Project\features.npy"
labels_file = r"D:\Data set\Project\labels.npy"
model_file = r"D:\Data set\Project\trained_model.pkl"

# Load features and labels
try:
    features = np.load(features_file)
    labels = np.load(labels_file)
    print(f"Loaded features shape: {features.shape}")
    print(f"Loaded labels shape: {labels.shape}")
except FileNotFoundError as e:
    print(f"Error: {e}. Ensure Step 4 completed successfully.")
    exit()
except Exception as e:
    print(f"Error loading features/labels: {e}")
    exit()

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42, stratify=labels
)
print(f"Training set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
try:
    model.fit(X_train, y_train)
    print("Model training complete.")
except Exception as e:
    print(f"Error training model: {e}")
    exit()

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy on test set: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the trained model
try:
    joblib.dump(model, model_file)
    print(f"Saved trained model to {model_file}")
except Exception as e:
    print(f"Error saving model: {e}")
    exit()

print("Step 5: Model Training complete.")