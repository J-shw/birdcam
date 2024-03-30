import RPi.GPIO as io
from modules.sysLogger import logger
import modules.camera as camera_commands
import functools

running = False

def last():
    return camera_commands.last_trigger

def start():
    global running

    running = True

    camera = camera_commands.creat_cam();
    if camera != None:
        io.setmode(io.BCM)
        channel = 4 
        io.setup(channel, io.IN, io.PUD_DOWN)

        # Create a partial function with camera object as an argument
        take_photo = functools.partial(camera_commands.take_photo, camera)

        # Assign the partial function to the rising edge event
        io.add_event_detect(channel, io.RISING, callback=take_photo, bouncetime=5000)

        try:
            logger.info("Waiting for motion")
            while running:
                pass

        except KeyboardInterrupt:
            running = False
            print("Exiting...")
        
        finally:
            logger.info('Ending motion detection')
            io.cleanup()

def stop():
    global running
    running = False