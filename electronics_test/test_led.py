from gpiozero import PWMLED
from time import sleep

# Define the GPIO pin where the LED is connected
LED_PIN = 18

# Create a PWMLED object (this allows for PWM control of brightness)
led = PWMLED(LED_PIN)

# Define a function to control the brightness using PWM
def fade_led():
    while True:
        # Gradually increase the brightness
        for brightness in range(0, 101, 5):  # 0 to 100, step by 5
            led.value = brightness / 100  # LED value ranges from 0 to 1
            sleep(0.1)
        
        # Gradually decrease the brightness
        for brightness in range(100, -1, -5):  # 100 to 0, step by -5
            led.value = brightness / 100  # LED value ranges from 0 to 1
            sleep(0.1)

try:
    fade_led()
except KeyboardInterrupt:
    print("Program interrupted")
