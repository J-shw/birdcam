#Import necessary libraries
import modules.startup
from flask import Flask, render_template, jsonify
from flask_caching import Cache
from waitress import serve
from modules.sysLogger import logger
import time, os, threading, motion, psutil

"""
Librarys to install:
pip install flask
pip install picamera2
pip install Pillow
pip install waitress
pip install psutil
pip install Flask-Caching
"""

#Initialize the Flask app
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


filePath = "/home/bird/static/data/photos/"
lowResPath = "/home/bird/static/data/photos/LR/"
highResPath = "/home/bird/static/data/photos/HR/"

print("\n\n")

time.sleep(0.2)

print("\n\n- - -Server started - - -\n")

thread = threading.Thread(target=motion.start)

# Start camera system on boot
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display_image/<image_folder>/<image>')
def display_image(image_folder, image):
    image_path = "data/photos/HR/" + image_folder + "/" + image
    image_loc = image_folder + "/" + image

    return render_template('display_image.html', image_path=image_path, image_name=image, image_loc=image_loc)

@app.route('/start', methods=['GET'])
def start_motion():
    global thread

    if motion.running:
        return(jsonify(status=200, data=None))
    else:
        try:
            thread.start()
            return(jsonify(status=200, data=None))
        except Exception as e:
            logger.critical(e)
            return(jsonify(status=200, data=str(e)))



@app.route('/end', methods=['GET'])
def stop_motion():
    global thread
    try:
        motion.stop()
    except Exception as e:
        logger.error(e)
        return(jsonify(status=400, data=str(e)))
    else:
        return(jsonify(status=200, data=None))
    finally:
        thread.join()

@app.route('/lowResImg', methods=['GET'])
def lowResImg_loc():
    storage = []

    try:
        files_and_directories = os.listdir(lowResPath)
        directories = [d for d in files_and_directories if os.path.isdir(os.path.join(lowResPath, d))]
        for d in directories:
            current = []
            current.append(d)
            newFilePath = str(lowResPath) + str(d)
            files_and_directories = os.listdir(newFilePath)
            files = [f for f in files_and_directories if os.path.isfile(os.path.join(newFilePath, f))]
            
            if len(files) == 0: return(jsonify(status=404, data="No files found"))
            for f in files:
                current.append(f)

            sorted_current = [current[0]] + sorted(current[1:], key=lambda x: x.split('.')[0], reverse=True)
            storage.append(sorted_current)
    except Exception as e:
        logger.error(e)
        return(jsonify(status=500, data=str(e)))
    
    sorted_storage = sorted(storage, key=lambda x: x[0], reverse=True)

    return jsonify(status=200, data=sorted_storage)

@app.route('/data', methods=['GET'])
def data():
    
    freq = psutil.cpu_freq()
    disk = psutil.disk_usage('/')

    cpuTemp = round(psutil.sensors_temperatures()['cpu_thermal'][0].current, 2)

    cpuFreq = round(freq.current, 2)

    totalDisk = round(disk.total / (1024*1024*1024), 2) #GB
    usedDisk = round(disk.used / (1024*1024*1024), 2) #GB

    last = motion.last()
    
    
    deviceData = [cpuTemp,cpuFreq,totalDisk,usedDisk]

    return jsonify(data=[last,deviceData], status=200) # Return data

@app.route('/delete_image/<image_folder>/<image>', methods=['GET'])
def deleteImage(image_folder, image):
    # delete the file
    try:
        os.remove(lowResPath+"/"+image_folder+"/"+image)
        os.remove(highResPath+"/"+image_folder+"/"+image)
    except Exception as e:
        logger.error(e)
        return  jsonify(data=str(e), status=500)
    return jsonify(data=None, status=200)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)