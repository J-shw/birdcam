import os

storage = []
lowResPath = f"{os.getcwd()}/static/data/photos/LR/"
files_and_directories = os.listdir(lowResPath)
directories = [d for d in files_and_directories if os.path.isdir(os.path.join(lowResPath, d))]
for d in directories:
    current.append(d)
    newFilePath = str(lowResPath) + str(d)
    files_and_directories = os.listdir(newFilePath)
    files = [f for f in files_and_directories if os.path.isfile(os.path.join(newFilePath, f))]
    
    if len(files) == 0: print('No files found')
    file_list
    for f in files:
        current.append(f)

    sorted_current = [current[0]] + sorted(current[1:], key=lambda x: x.split('.')[0], reverse=True)
    storage.append(sorted_current)


sorted_storage = sorted(storage, key=lambda x: x[0], reverse=True)
print(sorted_storage)