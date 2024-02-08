import json
import os
import pprint
import random
import string
import subprocess
import time
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
import tkinter as tk
from tkinter import filedialog

capabilities = dict(
    platformName='Android',
    deviceName='emulator-5554',
    language='en',
    locale='US'
)


class Product:
    def __init__(self, title, description, price, images):
        self.title = title
        self.description = description
        self.price = price
        self.images = images


app_paths = dict(
    main_page_open_path='//android.widget.TextView[@content-desc="OfferUp"]',
    post_icon='//com.horcrux.svg.SvgView[@resource-id="Post"]',
    post_title='//android.widget.EditText[@resource-id="post-flow-screen.1.listing-title.input.text-entry"]',
    post_description='//android.widget.EditText[@resource-id="post-flow-screen.1.description.input"]',
    image_elements='//android.widget.ImageView[resource-id="ucl.image"]',
    image_parent_elements='//android.view.ViewGroup[contains(@resource-id, "post-flow-select-photos-screen.item")]',
    select_photo_button='//android.widget.TextView[@text="Select photo"]',
    next_button="//android.widget.Button[contains(@resource-id, 'post-flow-screen.{}') and contains(@resource-id, '.next.button')]",
    post_button="//android.widget.Button[contains(@resource-id, 'post-flow-screen.') and contains(@resource-id, '.post.button')]",
    done_button='//android.widget.Button[@resource-id="post-flow-select-photos-screen.done.button"]',
    condition_button='//android.widget.Button[@content-desc="Condition"]',
    new='//android.widget.TextView[@text="New"]',
    price='//android.widget.EditText[@resource-id="post-flow.3.price.input.text-entry"]',
    current_condition='//android.widget.TextView[@resource-id="condition-displayValue"]',
    close_shipping='//android.widget.Switch[@resource-id="post-flow.4.shell-and-ship.flex-row.right-notification.toggle"]',
    close_button='//android.widget.Button[@resource-id="post-flow.shipping-ftue.navigation-bar.close.touchable-opacity"]',
    alternate_close_button='//android.view.ViewGroup[@resource-id="post-flow-screen.5.navigation-bar.right-items"]',
    post_another_item='//android.widget.Button[@resource-id="post-flow.5.post-another-item.button"]'
)

appium_server_url = 'http://localhost:4723/wd/hub'

key_codes = {
    'a': 29, 'b': 30, 'c': 31, 'd': 32, 'e': 33, 'f': 34, 'g': 35, 'h': 36,
    'i': 37, 'j': 38, 'k': 39, 'l': 40, 'm': 41, 'n': 42, 'o': 43, 'p': 44,
    'q': 45, 'r': 46, 's': 47, 't': 48, 'u': 49, 'v': 50, 'w': 51, 'x': 52,
    'y': 53, 'z': 54, '0': 7, '1': 8, '2': 9, '3': 10, '4': 11, '5': 12,
    '6': 13, '7': 14, '8': 15, '9': 16, ' ': 62
    # Add more mappings if needed
}


class OfferUp:
    def __init__(self) -> None:
        self.driver = webdriver.Remote(
            appium_server_url, options=AppiumOptions().load_capabilities(capabilities))

        self.products = []

    def choose_json_folder(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(
            title="Select a JSON file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        return file_path

    def load_products(self, json_path):
        with open(json_path, 'r') as file:
            data = json.load(file)
            for item in data:
                product = Product(
                    title=item["title"],
                    description=item["description"],
                    price=item["price"],
                    images=item["images"]
                )
                self.products.append(product)

    def open_app(self):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, app_paths.get('main_page_open_path'))))
        el.click()

    def open_post(self):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, app_paths.get('post_icon'))))
        el.click()

    def title(self, title="-"):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, app_paths.get('post_title'))))

        # Clear the existing text
        el.clear()

        # Then send the new keys
        el.send_keys(title)

    def description(self, description="-"):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, app_paths.get('post_description'))))

        el.clear()

        el.send_keys(description)

    def click_select_photo(self):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, app_paths.get('select_photo_button'))))
        el.click()

    def close_button_if_exist(self):
        wait = WebDriverWait(self.driver, 3)

        try:
            close_button_el = wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, app_paths.get('close_button'))))
            close_button_el.click()
        except TimeoutException:
            pass

    def change_condition(self):
        wait = WebDriverWait(self.driver, 6)

        current_condition_el = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, app_paths.get('current_condition'))))
        current_condition = current_condition_el.text
        print(current_condition)

        if current_condition != 'New':
            condition_button = wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, app_paths.get('condition_button'))))
            condition_button.click()

            new_button = wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, app_paths.get('new'))))
            new_button.click()

    def close_button_if_exist(self):
        wait = WebDriverWait(self.driver, 3)

        try:
            close_button_el = wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, app_paths.get('close_button'))))
            close_button_el.click()
        except TimeoutException:
            try:
                close_button_el = wait.until(EC.element_to_be_clickable(
                    (AppiumBy.XPATH, app_paths.get('alternate_close_button'))))
                close_button_el.click()
            except TimeoutException:
                pass

    def click_post_another_item(self):
        try:
            wait = WebDriverWait(self.driver, 10)

            post_another_item_button = wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, app_paths.get('post_another_item'))))
            post_another_item_button.click()
        except:
            pass

    def close_shipping(self):
        try:
            wait = WebDriverWait(self.driver, 10)

            el = wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, app_paths.get('close_shipping'))))
            el.click()
        except:
            return

    def price(self, price):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, app_paths.get('price'))))

        el.send_keys(price)

    def select_images_by_count(self, count):
        wait = WebDriverWait(self.driver, 3)  # Reduced wait time

        parent_elements = wait.until(EC.presence_of_all_elements_located(
            (AppiumBy.XPATH, app_paths.get('image_parent_elements'))))

        for element in parent_elements[:count]:
            if wait.until(lambda driver: element.is_displayed() and element.is_enabled()):
                element.click()

    def click_post_button(self):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, app_paths.get('post_button'))))
        el.click()

    def click_all_images(self):
        image_elements = self.driver.find_elements(
            AppiumBy.XPATH, app_paths.get('image_elements'))

        pprint.pprint(image_elements)
        for image in image_elements:
            image.click()

    def write(self, text):
        for char in text.lower():
            key_code = key_codes.get(char)
            if key_code:
                self.driver.press_keycode(key_code)
            else:
                print(f"No key code found for character '{char}'")
        pass

    def click_done_button(self):
        done_button = self.driver.find_element(
            AppiumBy.XPATH, app_paths.get('done_button'))
        done_button.click()

    def click_next_button(self, number: str = ''):
        wait = WebDriverWait(self.driver, 15)

        # Format the XPath string with the given number
        next_button_xpath = app_paths.get('next_button').format(number)

        # Wait until the 'Next' button is clickable, then click it
        next_button = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, next_button_xpath)))
        next_button.click()

    def click_pos(self, x, y):
        TouchAction(self.driver).tap(x=x, y=y).perform()

    def upload_images_to_device(self, images):
        for image in images:
            # Generate a random filename of 10 lowercase letters and numbers
            random_filename = ''.join(random.choices(
                string.ascii_lowercase + string.digits, k=10))

            # Append the original file extension to maintain the format
            file_extension = os.path.splitext(image)[1]
            random_filename_with_extension = random_filename + file_extension

            # Construct the destination path
            destination_path = f"/sdcard/Pictures/{random_filename_with_extension}"

            # Upload the image
            subprocess.run(
                ["adb", "push", image, destination_path], shell=True)

            # Trigger the media scanner
            subprocess.run(["adb", "shell", "am", "broadcast", "-a",
                            "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{destination_path}"], shell=True)

    def delete_all_images(self, images):
        for image in images:
            filename = os.path.basename(image)  # Extracts just the filename
            destination_path = f"/sdcard/Pictures/{filename}"
            subprocess.run(
                ["adb", "shell", "rm", destination_path], shell=True)

    def close_driver(self):
        self.driver.quit()


def main():

    offerUp = OfferUp()
    json_path = offerUp.choose_json_folder()
    if json_path:
        offerUp.load_products(json_path)
        # offerUp.open_app()

        for product in offerUp.products:

            offerUp.upload_images_to_device(product.images)
            time.sleep(10)
            offerUp.open_post()
            time.sleep(5)
            offerUp.title(product.title)
            offerUp.description(product.description)
            offerUp.click_select_photo()
            time.sleep(5)
            offerUp.select_images_by_count(len(product.images))
            offerUp.click_done_button()
            time.sleep(10)
            offerUp.click_next_button()
            time.sleep(10)
            offerUp.click_next_button(2)

            def round_price(price): return round(int(
                price) / 5) * 5 if round(int(price) / 5) * 5 != 0 or int(price) == 0 else int(price)

            # Use the lambda function to set the price
            rounded_price = round_price(product.price)
            offerUp.price(rounded_price)

            time.sleep(0.3)
            offerUp.click_next_button(3)
            offerUp.close_shipping()
            offerUp.click_post_button()
            time.sleep(5)
            offerUp.close_button_if_exist()
            time.sleep(5)
            offerUp.close_button_if_exist()
            time.sleep(2)
            offerUp.click_post_another_item()
            # offerUp.delete_all_images(product.images)

        offerUp.close_driver()


main()
