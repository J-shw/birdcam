import RPi.GPIO as io

io.setmode(io.BCM)
channel = 4 
io.setup(channel, io.IN, io.PUD_DOWN)

while True:
    if io.input(channel) == 1:
        print('Motion!')
    else:
        print('None')