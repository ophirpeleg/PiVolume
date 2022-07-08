import board
import digitalio

dirPin = digitalio.DigitalInOut(board.D17)
stepPin = digitalio.DigitalInOut(board.D18)
dirPin.direction = digitalio.Direction.INPUT
stepPin.direction = digitalio.Direction.INPUT

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



