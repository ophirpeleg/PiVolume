import board
import digitalio
import os
import os.path

dirPin = digitalio.DigitalInOut(board.D17)
# pushPin = digitalio.DigitalInOut(board.D16)
stepPin = digitalio.DigitalInOut(board.D18)

dirPin.direction = digitalio.Direction.INPUT
stepPin.direction = digitalio.Direction.INPUT
volumeInterval = 50

dirPin.pull = digitalio.Pull.UP
stepPin.pull = digitalio.Pull.UP
previousValue = True

print("Welcome")
print(f"{stepPin.value} step pin value, {dirPin.value} dir pin value")

is_on = True

while is_on:
    if previousValue != stepPin.value:
        print("Welcome2")
        if stepPin.value == False:
            print("Welcome3")
            if dirPin.value == False:
                print("Right")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}+")
            else:
                print("Left")
                os.system(f"amixer -c 0 set Headphone {volumeInterval}-")
        previousValue = stepPin.value



