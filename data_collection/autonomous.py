import time, libcamera
from picamera2 import Picamera2, Preview
from gpiozero import PWMLED
from gpiozero import LED
from time import sleep
import datetime

# Define the GPIO pins
LED_PIN = 18
PUMP_PIN = 17

# Create LED and Relay objects for control
led = PWMLED(LED_PIN)
led_brightness = 0.05
pump = LED(PUMP_PIN)

# create and configure the camera
picam = Picamera2()
config = picam.create_still_configuration(main={"size": (9152, 6944)})
picam.configure(config)

# main loop
try:
	picam.start()
	# turn the pump on for 1 minutes
	pump.on()
	print("Pump is ON")
	sleep(60)
	
	# turn the pump off
	pump.off()
	print("Pump is OFF")
	sleep(1)
	
	# turn the LED on
	led.value = led_brightness
	print("LED is ON")
	sleep(1)
	
	# take a picture
	current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
	file_path = f"img/{current_time}.jpg"
	picam.capture_file(file_path)
	print(f"Image taken and saved as {file_path}")
	sleep(1)
	
	# turn the LED off
	led.value = 0
	print("LED is OFF")
	sleep(1)
        
        
except KeyboardInterrupt:
	picam.close()
	print("Program interrupted by user")
