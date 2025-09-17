import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_still_configuration(main={"size": (9152, 6944)})
picam.configure(config)

# picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(2)
picam.capture_file("test-python.jpg")

picam.close()
