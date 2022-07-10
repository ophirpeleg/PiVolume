import board
import digitalio
import os
import os.path
import time
import busio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

### OLED Define ###

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('/home/smartmiror/repo/PiVolume/PixelOperator.ttf', 16)
# font = ImageFont.load_default()

### OLED Define END ###

### encoder define ###
state = 1


def millis():
    return time.monotonic() * 1000


def long_press(stat):
    if stat == 1:
        stat = 0
    else:
        stat = 1
    return stat

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

### oled define end ###

while is_on:
    ### OLED ###
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell=True)
    cmd = "amixer -c 0 sget Headphone"
    VOL = str(subprocess.check_output(cmd, shell=True))
    VOL = VOL[VOL.find("%") - 2:VOL.find("%")]
    cmd = "amixer -c 0 sget Headphone"
    MUTE = str(subprocess.check_output(cmd, shell=True))
    MUTE = MUTE[-6:-4]

    if MUTE == "on":
        mute = "off"
    else:
        mute = "on"

    if state == 1:
        draw.text((0, 0), "IP: " + str(IP, 'utf-8'), font=font, fill=255)
        draw.text((0, 16), str(CPU, 'utf-8') + "LA", font=font, fill=255)
        draw.text((0, 48), str(Disk, 'utf-8'), font=font, fill=255)
        draw.text((80, 16), str(temp, 'utf-8'), font=font, fill=255)
        draw.text((0, 32), str(MemUsage, 'utf-8'), font=font, fill=255)
    else:
        draw.text((0, 0), "Volume: " + str(VOL), font=font, fill=255)
        draw.text((70, 0), "Mute: " + str(mute), font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(.1)

    ### OLED ###

    if pushPin.value == 0:
        pressTime = millis()
        time.sleep(0.2)
        longPress = False

        while pushPin.value == 0:
            if millis() - pressTime > 1000 and not longPress:
                longPress = True
                state = long_press(state)

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
