from modules.sysLogger import logger
from picamera2 import Picamera2
from libcamera import controls
from PIL import Image
import time, datetime, os

last_trigger = None

class camera_data:
    filePath = "/home/bird/static/data/photos/" # Make sure there is a HR and LR folder to save High res and Low res photos

def creat_cam():
    try:
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)})
        picam2.configure(camera_config)
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        #picam2.set_controls({
        #   "AfMode": controls.AfModeEnum.Continuous,
        #   "ExposureTime": "auto"
        #})

        return picam2
    except Exception as e:
        logger.critical(e)
        return None
    finally:
        logger.info('Camera created')

def take_photo(camera):
    global last_trigger

    logger.info('Taking photo')

    current_time = datetime.datetime.now()
    last_trigger = current_time
    formatted_date = current_time.strftime("%Y-%m-%d")
    formatted_time = current_time.strftime("%H:%M:%S")

    try: 
        hr_filepath = str(camera_data.filePath)+"HR/" + str(formatted_date)
        lr_filepath= str(camera_data.filePath)+"LR/" + str(formatted_date)
        os.makedirs(hr_filepath, exist_ok=True)
        os.makedirs(lr_filepath, exist_ok=True)
    except Exception as e: logger.error(f'Failed to create filepath: {e}')

    try:
        camera.start()
        hr_file = f"{hr_filepath}/{formatted_time}.jpg"
        lr_file = f"{lr_filepath}/{formatted_time}.jpg"
        camera.capture_file(hr_file)
    except Exception as e:
        logger.critical(f'Failed to take photo: {e}')
    finally: camera.stop()

    try:
        # Resize the high-resolution image to create the low-resolution image
        highres_image = Image.open(hr_file)
        lowres_image = highres_image.resize((640, 480))
        lowres_image.save(lr_file)
    except Exception as e: 
        logger.error(f"Failed to resize photo: {e}")
