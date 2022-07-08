import board
import digitalio

dirPin = digitalio.DigitalInOut(board.GP17)
stepPin = digitalio.DigitalInOut(board.GP18)
dirPin.direction = digitalio.Durection.INPUT
stepPin.direction = digitalio.Durection.INPUT

dirPin.pull = digitalio.Pull.UP
stepPin.pull = digitalio.Pull.UP
previousValue = True

while 1 == 1:
    if previousValue != stepPin.value:
        if stepPin.value == False:
            if dirPin.value == False:
                print("Left")
            else:
                print("Right")
        previousValue = stepPin.value



