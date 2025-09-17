import os
import time
from gpiozero import PWMLED, LED
from picamera2 import Picamera2
import cv2

# Setup
LED_PIN = 18
RELAY_PIN = 17
GREEN_DIR = "./data/turbidity/green"
ORANGE_DIR = "./data/turbidity/orange"
brightness = 0.02
led = PWMLED(LED_PIN)
relay = LED(RELAY_PIN)
picam = Picamera2()
config = picam.create_still_configuration(main={"size": (9152, 6944)})
picam.configure(config)

def get_next_image_number():
    green_files = [f for f in os.listdir(GREEN_DIR) if f.startswith("image") and f.endswith(".jpg")]
    numbers = []
    for f in green_files:
        try:
            num = int(f.replace("image", "").replace(".jpg", ""))
            numbers.append(num)
        except ValueError:
            continue
    return max(numbers, default=0) + 1

def capture_image(filename):
    picam.start()
    time.sleep(2)
    picam.capture_file(filename)
    # picam.close()

def wait_for_user(prompt, valid_inputs):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_inputs:
            return choice

# Main Loop
image_number = get_next_image_number()

try:
    while True:
        # Step 1: Turn on pump
        relay.on()
        print("Pump ON")
        time.sleep(3)

        # Step 2: Turn off pump
        relay.off()
        print("Pump OFF")
        time.sleep(10)

        # Step 3: Turn on LED
        led.value = brightness
        print("LED ON")
        time.sleep(2)

        # Step 4: Take a picture
        temp_filename = "./tmp.jpg"
        capture_image(temp_filename)
        print("PICTURE TAKEN")
        led.value = 0
        print("LED OFF")

        # Step 5: User choice to repeat or continue
        choice = wait_for_user("Repeat pump cycle (a) or continue to green save (b)? [a/b]: ", ["a", "b"])
        if choice == "a":
            continue

        # Step 6: Save image to green directory
        green_filename = os.path.join(GREEN_DIR, f"image{image_number}.jpg")
        os.rename(temp_filename, green_filename)
        print(f"Saved to {green_filename}")

        # Step 7: Wait for user input to proceed
        input("Press Enter to continue to LED ON for orange capture...")

        # Step 8: LED on
        led.value = brightness
        print("LED ON")
        time.sleep(2)

        # Step 9: Capture orange image
        capture_image(temp_filename)
        #choice = wait_for_user("Repeat orange capture (a) or continue to save (b)? [a/b]: ", ["a", "b"])
        #while choice == "a":
        #    time.sleep(2)
        #    capture_image(temp_filename)
        #    choice = wait_for_user("Repeat orange capture (a) or continue to save (b)? [a/b]: ", ["a", "b"])

        led.value = 0
        print("LED OFF")

        # Step 10: Save to orange directory
        orange_filename = os.path.join(ORANGE_DIR, f"image{image_number}.jpg")
        os.rename(temp_filename, orange_filename)
        print(f"Saved to {orange_filename}")

        # Step 11: Loop back
        image_number += 1

except KeyboardInterrupt:
    print("Program interrupted by user.")
    led.value = 0
    relay.off()
    cv2.destroyAllWindows()
