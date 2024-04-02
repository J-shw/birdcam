import os

# Setup initial empty folders if not present
folders = ['static/data/logs', 'static/data/photos', 'static/data/photos/HR', 'static/data/photos/LR'] 
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)