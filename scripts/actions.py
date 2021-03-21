import cv2
import pyautogui
import numpy as np
import os
import json
from scripts import utils
from scripts.utils import Point, ImagePosition

# import configuration

config = {}
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
def find_image(image_path, x_begin=0, y_begin=0, x_end=99999, y_end=99999, new_screenshot=True):
    img_template = cv2.imread(image_path)
    w, h = img_template.shape[:-1]
    if new_screenshot:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
    img_rgb = cv2.imread(screenshot_path)

    res = cv2.matchTemplate(img_rgb, img_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        if x_begin <= pt[0] <= x_end and y_begin <= pt[1] <= y_end:
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            # cv2.imwrite(temp_folder+'/found_colored.png', img_rgb)
            return pt[0], pt[1]
    return -1, -1


# returns coordinate of images
# success: returns x_coordinate, y_coordinate list
# failure: returns []
def find_images(image_path, x_begin=0, y_begin=0, x_end=99999, y_end=99999, new_screenshot=True):
    begin_p = Point(x_begin, y_begin)
    end_p = Point(x_end, y_end)

    img_template = cv2.imread(image_path)
    w, h = img_template.shape[:-1]
    if new_screenshot:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
    img_rgb = cv2.imread(screenshot_path)

    res = cv2.matchTemplate(img_rgb, img_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    result: list[ImagePosition] = []

    def already_found(min: Point, max: Point):
        result_list = [p for p in result if utils.overlapping_rect(min, max, p.min, p.max)
                       or utils.in_vicinity_pt(Point(int((min.x + max.x)/2), int((min.y + max.y) / 2)), p.min, p.max)]
        if result_list:
            return True
        return False

    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        if utils.in_vicinity_pt(Point(pt[0], pt[1]), begin_p, end_p) \
                and not already_found(Point(pt[0], pt[1]), Point(pt[0] + h, pt[1] + w)):
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            # cv2.imwrite(temp_folder+'/found_colored.png', img_rgb)
            result.append(ImagePosition(pt[0] + h / 2, pt[1] + w / 2, pt[0], pt[1], pt[0] + h, pt[1] + w))
    return result


# moves mouse to coordinate then click
def move_and_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(x, y)


# click on key from keyboard
def keyboard_stroke(key):
    pyautogui.press(key)


# moves mouse to coordinate
def moveTo(x, y):
    pyautogui.moveTo(x, y)


# clicks on image if found
# success: returns True
# failure: returns False
def click_on_image(image_path, x_begin=0, y_begin=0, x_end=99999, y_end=99999, new_screenshot=True):
    img_template = cv2.imread(image_path)
    w, h = img_template.shape[:-1]
    if new_screenshot:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
    img_rgb = cv2.imread(screenshot_path)

    res = cv2.matchTemplate(img_rgb, img_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        if x_begin <= pt[0] <= x_end and y_begin <= pt[1] <= y_end:
            btn_center_x = int(pt[0] + h / 2)
            btn_center_y = int(pt[1] + w / 2)
            pyautogui.moveTo(btn_center_x, btn_center_y)
            pyautogui.click(btn_center_x, btn_center_y)
            return True
    return False
