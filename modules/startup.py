import os

# Setup initial empty folders if not present
folders = ['static/data/photos/HR', 'static/data/photos/LR'] 
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)

from modules.sysLogger import logger # Must be imported after folder creation
# Clear temp folder
try:
    directory_path = 'static/data/temp/'
    # List all files in the directory
    files = os.listdir(directory_path)

    # Iterate over each file and remove it
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

except Exception as e:
    logger.error(f"Failed to clean temp folder: {e}")