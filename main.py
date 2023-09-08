#Import necessary libraries
from flask import Flask, render_template, jsonify
from flask_caching import Cache
from waitress import serve
import time, os, threading

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

debugMode = False
laptop = False

if laptop:
    filePath = "/Users/josh/Documents/Coding/Big Pi projects/Animal Camera/webApp/static/data/photos/"
else:
    import camera, psutil
    import RPi.GPIO as io

    filePath = "/home/josh/AnimaL-server/static/data/photos/"
    lowResPath = "/home/josh/AnimaL-server/static/data/photos/LR/"
    highResPath = "/home/josh/AnimaL-server/static/data/photos/HR/"

    # Set GPIO mode to BCM
    io.setmode(io.BCM)
    pir = 4

    # Set pir as input
    io.setup(pir, io.IN, io.PUD_DOWN)


print("\n\n")



time.sleep(0.2)

print("\n\n- - -Server started - - -\n")

def dprint(message):
    if debugMode:
        print(message)

def run_in_thread():
    camera.run()

thread = threading.Thread(target=run_in_thread)

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
def start():
    global thread
    function = camera.status() # return layout - [Status, Running, Crashed, Error]
    if function[1]:
        return(jsonify(status=200, data=None))
    else:
        try:
            thread.start()
            time.sleep(2)
            function = camera.status() # return layout - [Status, Running, Crashed, Error]
            if function[2]:
                return(jsonify(status=function[0], data=function[3]))
            else:
                    return(jsonify(status=200, data=None))

        except Exception as a:
            try:
                camera.run()
                time.sleep(0.5)
                function = camera.status() # return layout - [Status, Running, Crashed, Error]
                if function[2]:
                    return(jsonify(status=500, data=function[3]))
                else:
                    return(jsonify(status=200, data=None))
            except Exception as b:
                error = str(a) + " | " + str(b)
                return(jsonify(status=400, data=error))

@app.route('/end', methods=['GET'])
def end():
    global thread
    try:
        function = camera.end()
    except Exception as e:
        return(jsonify(status=400, data=str(e)))
    if function[0] != 200:
        return(jsonify(status=function[0], data=function[1]))
    else:
        return(jsonify(status=200, data=None))

@app.route('/status', methods=['GET'])
def status():
    try:
        function = camera.status() # return layout - [Status, Running, Crashed, Error]
    except Exception as e: return(jsonify(status=400, data = False, error=str(e)))

    if function[0] != 200: return(jsonify(status=function[0], data = False, error=function[3]))

    else: 
        if function[2]: # If state is crashed then...
            return(jsonify(status=200, data = False, error=function[3]))
        
        return(jsonify(status=200, data=function[1], error=False))

@app.route('/lowResImg', methods=['GET'])
def lowResImg_loc():
    storage = []

    try:
        files_and_directories = os.listdir(lowResPath)
        dprint(files_and_directories)
        directories = [d for d in files_and_directories if os.path.isdir(os.path.join(lowResPath, d))]
        dprint(directories)
        for d in directories:
            dprint("Here - " +str(d))
            current = []
            current.append(d)
            newFilePath = str(lowResPath) + str(d)
            files_and_directories = os.listdir(newFilePath)
            files = [f for f in files_and_directories if os.path.isfile(os.path.join(newFilePath, f))]
            dprint(files)
            for f in files:
                current.append(f)

            sorted_current = [current[0]] + sorted(current[1:], key=lambda x: x.split('.')[0], reverse=True)
            dprint(sorted_current)
            storage.append(sorted_current)
            dprint(storage)
    except Exception as e:
        dprint(str(e))
        return(jsonify(status=500, data=str(e)))
    
    dprint(storage)
    sorted_storage = sorted(storage, key=lambda x: x[0], reverse=True)
    dprint(sorted_storage)

    return jsonify(status=200, data=sorted_storage)

@app.route('/data', methods=['GET'])
def data():
    
    freq = psutil.cpu_freq()
    disk = psutil.disk_usage('/')

    cpuTemp = round(psutil.sensors_temperatures()['cpu_thermal'][0].current, 2)

    cpuFreq = round(freq.current, 2)

    totalDisk = round(disk.total / (1024*1024*1024), 2) #GB
    usedDisk = round(disk.used / (1024*1024*1024), 2) #GB

    last = camera.last()
    
    
    deviceData = [cpuTemp,cpuFreq,totalDisk,usedDisk]

    return jsonify(data=[last,deviceData], status=200) # Return data

@app.route('/delete_image/<image_folder>/<image>', methods=['GET'])
def deleteImage(image_folder, image):
    # delete the file
    try:
        os.remove(lowResPath+"/"+image_folder+"/"+image)
        os.remove(highResPath+"/"+image_folder+"/"+image)
    except Exception as e:
        return  jsonify(data=str(e), status=500)
    return jsonify(data=None, status=200)

if debugMode:
    app.run(host='0.0.0.0', port=8080, debug=True)
else:
    if __name__ == "__main__":
        serve(app, host="0.0.0.0", port=8080)