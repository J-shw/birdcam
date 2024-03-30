import os

# Setup initial empty folders if not present
folders = ['static/data/photos/HR', 'static/data/photos/LR', 'static/data/logs'] 
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)