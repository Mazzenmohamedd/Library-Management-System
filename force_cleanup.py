import shutil
import os
import time

path = r"c:\College\swe_project anti\swe_project\pages"

if os.path.exists(path):
    print(f"Removing {path}...")
    try:
        shutil.rmtree(path)
        print("Successfully removed pages directory.")
    except Exception as e:
        print(f"Error removing {path}: {e}")
else:
    print("pages directory does not exist.")
