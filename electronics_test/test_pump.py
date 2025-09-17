from gpiozero import LED
from time import sleep

# Set up the relay pin (connected to GPIO 17)
relay = LED(17)

try:
    while True:
        relay.on()  # Turn the relay on
        print("Relay is ON")
        sleep(2)
        
        relay.off()  # Turn the relay off
        print("Relay is OFF")
        sleep(2)

except KeyboardInterrupt:
    print("Program interrupted by user")
