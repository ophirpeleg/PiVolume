import board
import digitalio
import os
import os.path

dirPin = digitalio.DigitalInOut(board.D2)
pushPin = digitalio.DigitalInOut(board.D8)
stepPin = digitalio.DigitalInOut(board.D3)

dirPin.direction = digitalio.Direction.INPUT
stepPin.direction = digitalio.Direction.INPUT
volumeInterval = 50

dirPin.pull = digitalio.Pull.UP
stepPin.pull = digitalio.Pull.UP
pushPin.pull = digitalio.Pull.UP
previousValue = True

print("Welcome")
print(f"{stepPin.value} step pin value, {dirPin.value} dir pin value")
print(f"push pin value: {pushPin.value}")
is_on = True

while is_on:
    if pushPin.value == False:
        print("False")

    if previousValue != stepPin.value:
        if stepPin.value == False:
            if dirPin.value == False:
                print("Right")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}+")
            else:
                print("Left")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}-")
        previousValue = stepPin.value



