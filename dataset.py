import os
os.environ['KAGGLE_CONFIG_DIR'] = r"C:\Users\Alle Keerthi Harsha\Documents\.kaggle"
from kaggle.api.kaggle_api_extended import KaggleApi

# Authenticate using the kaggle.json in the folder you just set
api = KaggleApi()
api.authenticate()

print("Kaggle API authenticated successfully!")

# Download and unzip the dataset
api.dataset_download_files(
    "grassknoted/asl-alphabet",           # Dataset identifier
    path=r"C:\Users\Alle Keerthi Harsha\Documents\ASL",  # Where to save
    unzip=True                            # Automatically unzip
)

print("📥 Dataset downloaded and extracted!")

