import board
import digitalio
import os
import os.path

dirPin = digitalio.DigitalInOut(board.D17)
stepPin = digitalio.DigitalInOut(board.D18)
dirPin.direction = digitalio.Direction.INPUT
stepPin.direction = digitalio.Direction.INPUT
volumeInterval = 50

dirPin.pull = digitalio.Pull.UP
stepPin.pull = digitalio.Pull.UP
previousValue = True

while 1 == 1:
    if previousValue != stepPin.value:
        if stepPin.value == False:
            if dirPin.value == False:
                print("Right")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}+")
            else:
                print("Left")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}-")
        previousValue = stepPin.value



