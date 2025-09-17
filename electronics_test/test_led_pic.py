import time, libcamera
from picamera2 import Picamera2, Preview
from gpiozero import PWMLED
from time import sleep


# Define the GPIO pin where the LED is connected
LED_PIN = 18

# Create a PWMLED object (this allows for PWM control of brightness)
led = PWMLED(LED_PIN)

led.value = 0.5

picam = Picamera2()

config = picam.create_still_configuration(main={"size": (9152, 6944)})
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(2)
picam.capture_file("test-python.jpg")

picam.close()

