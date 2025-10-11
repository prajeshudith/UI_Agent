import os

def load_feature_files(folder_path):
    """Load and return the content of all .feature files in the specified folder"""
    feature_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".feature"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    feature_files.append(f.read())
    return feature_files