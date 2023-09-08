import time, datetime, os
import RPi.GPIO as io
from picamera2 import Picamera2
from libcamera import controls
from PIL import Image

debug = False
crash = [False, None]

wait = 1
filePath = "/home/bird/static/data/photos/" # Make sure there is a HR and LR folder to save High res and Low res photos
last_time = None

# Set GPIO mode to BCM
io.setmode(io.BCM)
pir = 4

# Set pir as input
io.setup(pir, io.IN, io.PUD_DOWN)

def dprint(message):
    if debug:
        print(message)

running = False

def run():
    global running
    global wait
    global last_time
    global filePath
    global crash
    global picam2

    time.sleep(2)

    try:
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)})
        picam2.configure(camera_config)
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        #picam2.set_controls({
        #   "AfMode": controls.AfModeEnum.Continuous,
        #   "ExposureTime": "auto"
        #})

    except Exception as e:
        dprint("Error - " + str(e))
        if debug != True:
            running = False
            crash = [True, str(e)]
            return (0)
        
    time.sleep(1)
    if running == False:
        running = True
        crash = [False, None]
        while running:
            time.sleep(wait)

            if io.input(pir) == 1:
                wait = 0.1
                dprint("Motion")
                current_time = datetime.datetime.now()
                if last_time != None:
                    time_gap = current_time - last_time
                else: 
                    time_gap = current_time - current_time
                    last_time = datetime.datetime.now()

                if time_gap.total_seconds() >= 5:
                    last_time =  datetime.datetime.now()
                    dprint("Photo taken")
                    formatted_date = current_time.strftime("%Y-%m-%d")
                    formatted_time = current_time.strftime("%H:%M:%S")

                    try: 
                        hr_filepath = str(filePath)+"HR/" + str(formatted_date)
                        lr_filepath= str(filePath)+"LR/" + str(formatted_date)
                        os.makedirs(hr_filepath, exist_ok=True)
                        os.makedirs(lr_filepath, exist_ok=True)
                    except: dprint("Failed to create file")

                    try:
                        picam2.start()
                    except Exception as e:
                        crash = [True, str(e)] 
                        dprint("Failed to start camera")

                    try:
                        hr_file = hr_filepath + "/" + str(formatted_time) + ".jpg"
                        lr_file = lr_filepath + "/" + str(formatted_time) + ".jpg"
                        picam2.capture_file(hr_file)
                    except Exception as e: 
                        dprint("Failed to take photo - " + str(e))
                    
                    try:
                        picam2.stop()
                    except Exception as e:
                        crash = [True, str(e)] 
                        dprint("Failed to close camera")

                    try:
                        # Resize the high-resolution image to create the low-resolution image
                        highres_image = Image.open(hr_file)
                        lowres_image = highres_image.resize((640, 480))
                        lowres_image.save(lr_file)

                    except Exception as e: 
                        dprint("Failed to resize photo - " + str(e))
            else:
                dprint("No motion")
                wait = 1
    else: return(0)

def end():
    global running
    
    if running:
        try:
            running = False
            global picam2
            picam2.stop()
            picam2.close()
        except Exception as e: return([400, str(e)])

    return([200, "Script stopped"])

def last():
    if last_time != None:
        formatted_date = last_time.strftime("%Y-%m-%d")
        formatted_time = last_time.strftime("%H:%M:%S")

        data = [formatted_date, formatted_time]
        return(data)
    else:
        return None

def status(): # return layout - [Status, Running, Crashed, Error]
    global crash

    if crash[0] != True:
        try:
            global running
            return ([200, running, False])
        except Exception as e:
            return([500, None, True, str(e)])
    else:
        return ([200, False, crash[0], crash[1]])
