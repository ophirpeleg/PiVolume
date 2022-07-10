import board
import digitalio
import os
import os.path
import time


def millis():
    return time.monotonic() * 1000


def long_press():
    os.system(f"amixer -c 0 set Headphone unmute")
    os.system(f"amixer -c 0 set Headphone 0")
    return False

os.system(f"amixer -c 0 set Headphone unmute")
mute = False

dirPin = digitalio.DigitalInOut(board.D27)
pushPin = digitalio.DigitalInOut(board.D17)
stepPin = digitalio.DigitalInOut(board.D22)

dirPin.direction = digitalio.Direction.INPUT
pushPin.direction = digitalio.Direction.INPUT
stepPin.direction = digitalio.Direction.INPUT
volumeInterval = 100

dirPin.pull = digitalio.Pull.UP
stepPin.pull = digitalio.Pull.UP
pushPin.pull = digitalio.Pull.UP
previousValue = True

print("Welcome")
print(f"{stepPin.value} step pin value, {dirPin.value} dir pin value")
print(f"push pin value: {pushPin.value}")
is_on = True

while is_on:
    if pushPin.value == 0:
        pressTime = millis()
        time.sleep(0.2)
        longPress = False

        while pushPin.value == 0:
            if millis() - pressTime > 1000 and not longPress:
                longPress = True
                mute = long_press()

        if not longPress:  # short press define
            if mute:
                os.system(f"amixer -c 0 set Headphone unmute")
                mute = False
            else:
                os.system(f"amixer -c 0 set Headphone mute")
                mute = True

    if previousValue != stepPin.value:
        if stepPin.value == False:
            if dirPin.value == False:
                print("Right")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}+")
            else:
                print("Left")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}-")
        previousValue = stepPin.value
