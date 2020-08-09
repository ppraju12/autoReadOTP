import numpy
import pytesseract
import re
import time
import clipboard
import cv2

from PIL import ImageGrab
from datetime import datetime


def im_to_string(start_x, start_y, end_x, end_y):
    # ImageGrab-To capture the screen image in a loop.
    # Bbox used to capture a specific area.
    cap = ImageGrab.grab(bbox=(start_x, start_y, end_x, end_y))

    # Converted the image to monochrome for it to be easily
    # read by the OCR and obtained the output String.
    tes_string = pytesseract.image_to_string(
        cv2.cvtColor(numpy.array(cap), cv2.COLOR_BGR2GRAY),
        lang='eng')

    # Search for the substrings  relevant for OTP
    if tes_string.lower().find('otp') != -1 or \
            tes_string.lower().find('verification') != -1 or \
            tes_string.lower().find('code') != -1:

        # Find all the consecutive numbers in the string
        matches = re.findall(r'\d+', tes_string)

        if matches:
            # Sort the list in the descending order of the length of elements
            matches_sorted = sorted(matches, key=len, reverse=True)
            for match in matches_sorted:
                # Search for the OTP with 6 or 4 digit number
                if len(match) == 6 or len(match) == 4:
                    otp = match
                    current_time = datetime.now().strftime("%I:%M %p")
                    print("OTP: " + otp + " captured at " + current_time)
                    clipboard.copy(otp)
                    break


# Path of tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\*********\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

print('Reading OTPs from Notifications for every 5 secs...')
while True:
    # Calling the function with the window co-ordinates of the Pop-up Notification
    im_to_string(1361, 695, 1870, 999)
    # Calling the function with the window co-ordinates of the message in Notification Tray
    im_to_string(1320, 88, 1892, 399)
    time.sleep(5)
