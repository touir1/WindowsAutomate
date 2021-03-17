import cv2
import pyautogui
import numpy as np
import os
import json

# import configuration
config = {
    "temp_folder": "./temp",
    "actions_pause_interval": .5,
    "image_recon_threshold": .8
}
if os.path.exists('../config.json'):
    config = json.load(open('../config.json', ))

# configurations
pyautogui.PAUSE = config['actions_pause_interval'] or .5
threshold = config['image_recon_threshold'] or .8
temp_folder = config['temp_folder'] or './temp'
screenshot_path = temp_folder + '/screenshot.png'

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder, exist_ok=True)


# returns coordinate of image
# success: returns x_coordinate, y_coordinate
# failure: returns -1, -1
def find_image(image_path):
    img_template = cv2.imread(image_path)
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    img_rgb = cv2.imread(screenshot_path)

    res = cv2.matchTemplate(img_rgb, img_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        return pt[0], pt[1]
    return -1, -1


# moves mouse to coordinate then click
def move_and_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(x, y)


# clicks on image if found
# success: returns True
# failure: returns False
def click_on_image(image_path):
    img_template = cv2.imread(image_path)
    w, h = img_template.shape[:-1]
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    img_rgb = cv2.imread(screenshot_path)

    res = cv2.matchTemplate(img_rgb, img_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        btn_center_x = int(pt[0] + h / 2)
        btn_center_y = int(pt[1] + w / 2)
        pyautogui.moveTo(btn_center_x, btn_center_y)
        pyautogui.click(btn_center_x, btn_center_y)
        return True
    return False