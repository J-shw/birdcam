#Import necessary libraries
import modules.startup
import modules.camera as camera_controls
import modules.motion as motion
from modules.sysLogger import logger
from flask import Flask, render_template, jsonify, send_from_directory
from waitress import serve
import time, os, threading, psutil

"""
Librarys to install:
pip install flask
pip install picamera2
pip install Pillow
pip install waitress
pip install psutil
pip install requests
"""

#Initialize the Flask app
app = Flask(__name__)

filePath = f"{os.getcwd()}/static/data/photos/"
lowResPath = f"{os.getcwd()}/static/data/photos/LR/"
highResPath = f"{os.getcwd()}/static/data/photos/HR/"

logger.info('Starting server')

thread = threading.Thread(target=motion.start)

# Start camera system on boot
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manual/photo')
def take_photo():
    try:
        camera_controls.take_photo()
    except Exception as e:
        logger.error(e)
        return(jsonify(status=500, data=str(e)))
    return(jsonify(status=200, data=None))

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
            newFilePath = str(lowResPath) + str(d)
            files_and_directories = os.listdir(newFilePath)
            files = [f for f in files_and_directories if os.path.isfile(os.path.join(newFilePath, f))]
            
            files_list = []
            for f in files:
                files_list.append(f)
            
            current = {
                "folder": d,
                "files": sorted(files_list[1:], key=lambda x: x.split('.')[0], reverse=True)
            }

            storage.append(current)
    except Exception as e:
        logger.error(e)
        return(jsonify(status=500, data=str(e)))

    return jsonify(status=200, data=storage)

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

@app.route('/download/image/<image_folder>/<image>', methods=['GET'])
def downloadImage(image_folder, image):

    image_path = os.path.join(highResPath, image_folder, image)

    # Check if the file exists
    if os.path.isfile(image_path):
        # Serve the file for download
        return send_from_directory(directory=os.path.join(highResPath, image_folder), filename=image, as_attachment=True)
    else:
        # If the file does not exist, return a 404 error
        return "File not found", 404


if __name__ == "__main__":
    try:
        serve(app, host="0.0.0.0", port=8080)
    except Exception as e:
        logger.critical(f"failed to start sever: {e}")