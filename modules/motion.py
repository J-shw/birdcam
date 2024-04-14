import RPi.GPIO as io
from modules.sysLogger import logger
import modules.camera as camera_commands
import time

running = False

def last():
    return camera_commands.last_trigger

def motion_detected():
    logger.info('Motion detected')
    camera_commands.take_photo()

def start():
    global running

    logger.info('Camera started')

    running = True

    
    io.setmode(io.BCM)
    channel = 4 
    io.setup(channel, io.IN, io.PUD_DOWN)

    # Assign the partial function to the rising edge event
    io.add_event_detect(channel, io.RISING, callback=motion_detected, bouncetime=5000)

    try:
        logger.info("Waiting for motion")
        while running:
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Exiting...")
    
    finally:
        logger.info('Ending motion detection')
        stop()
        io.cleanup()

def stop():
    global running
    logger.info('Camera stopped')
    running = False