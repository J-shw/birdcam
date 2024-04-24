from modules.sysLogger import logger
import modules.webhook as webhook
from picamera2 import Picamera2, Preview
from libcamera import controls
from PIL import Image
import time, datetime, os, json

last_trigger = None

class camera_data:
    filePath = f"{os.getcwd()}/static/data/photos/" # Make sure there is a HR and LR folder to save High res and Low res photos

try:
    camera = Picamera2()
    camera_config = camera.create_still_configuration(main={"size": (4608, 2592), "format": "BGR888"})
    camera.configure(camera_config)
    camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    #camera.start_preview(Preview.DRM)
    #camera.set_controls({
    #   "AfMode": controls.AfModeEnum.Continuous,
    #   "ExposureTime": "auto"
    #})
    logger.info('Camera created')
except Exception as e:
    logger.critical(f'Failed to create camera: {e}')
    camera = None

def take_photo(channel='manual'):
    try:
        with open('static/data/configs/config.json') as config_file:
            configData = json.load(config_file)
    except Exception as e:
        logger.critical(e)

    global last_trigger
    global camera
    global configData
    if camera == None: 
        logger.warning('No camera set')
        return

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
    logger.info('Photo taken!')

    if configData['alerts']:
        webhook.send(configData['webhook']['server'], configData['webhook']['eventKey'])