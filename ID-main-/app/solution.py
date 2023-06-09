from random import random as rdm
import re
import os
from typing import List, Union
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
from loguru import logger
from app.captcha_resolver import CaptchaResolver
from app.settings import CAPTCHA_SINGLE_IMAGE_FILE_PATH
from app.utils import resize_base64_image


# 点击广告
class Solution(object):

    def __init__(self,url):
        os.system(r'start chrome --remote-debugging-port=9527  --incognito  --user-data-dir="F:\selenium"')
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("debuggerAddress", '127.0.0.1:9527')
        self.browser =webdriver.Chrome(options=self.options)
        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, 50)
        self.captcha_resolver = CaptchaResolver()


    def __del__(self):
        time.sleep(10)
        self.browser.close()    #6 关闭

    # 函数参数中的冒号是参数的类型建议符，告诉函数调用者希望传入的实参的类型。
    # 函数后面跟着的箭头是函数返回值的类型建议符，用来说明该函数返回的值是什么类型。
    def get_captcha_entry_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()    #5
        time.sleep(5)
        captcha_entry_iframe = self.browser.find_element(By.CSS_SELECTOR,
            'div > iframe')
        return captcha_entry_iframe

    def switch_to_captcha_entry_iframe(self) -> None:
        captcha_entry_iframe: WebElement = self.get_captcha_entry_iframe()  #4
        self.browser.switch_to.frame(captcha_entry_iframe)

    def get_captcha_content_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        captcha_content_iframe = self.browser.find_element(By.XPATH,
            '//iframe[contains(@title,"hCaptcha挑战的主要内容")]')
        return captcha_content_iframe

    def switch_to_captcha_content_iframe(self) -> None:
        captcha_content_iframe: WebElement = self.get_captcha_content_iframe()
        self.browser.switch_to.frame(captcha_content_iframe)

    def get_captcha_element(self) -> WebElement:
        captcha_element: WebElement = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.task-grid')))
        print(type(captcha_element))
        return captcha_element

    #1 检测图片大小是否可以破解， 2 校验验证码是否破解
    def detector_img(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.refresh button')))
        self.browser.find_element(By.CSS_SELECTOR, '.refresh button').click()

    def trigger_captcha(self) -> None:
        self.switch_to_captcha_entry_iframe()                #3
        captcha_entry = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#anchor #checkbox')))
        captcha_entry.click()
        time.sleep(3)
        self.switch_to_captcha_content_iframe()
        captcha_element: WebElement = self.get_captcha_element()
        if captcha_element.is_displayed:
            logger.debug('trigged captcha successfully')

    def get_captcha_target_text(self) -> WebElement:
        captcha_target_name_element: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.prompt-text')))
        return captcha_target_name_element.text

    def get_verify_button(self) -> WebElement:
        verify_button = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.button-submit')))
        return verify_button

    def get_is_successful(self):
        self.switch_to_captcha_entry_iframe()
        anchor: WebElement = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '#anchor #checkbox'
        )))
        checked = anchor.get_attribute('aria-checked')
        logger.debug(f'checked {checked}')
        return str(checked) == 'true'

    def verify_captcha(self):
        # get target text
        self.captcha_target_text = self.get_captcha_target_text()
        logger.debug(
            f'captcha_target_text {self.captcha_target_text}'
        )
        # extract all images
        single_captcha_elements = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '.task-image .image-wrapper .image')))
        resized_single_captcha_base64_strings = []
        for i, single_captcha_element in enumerate(single_captcha_elements):
            single_captcha_element_style = single_captcha_element.get_attribute(
                'style')
            pattern = re.compile('url\("(https.*?)"\)')
            match_result = re.search(pattern, single_captcha_element_style)
            single_captcha_element_url = match_result.group(
                1) if match_result else None
            logger.debug(
                f'single_captcha_element_url {single_captcha_element_url}')
            with open(CAPTCHA_SINGLE_IMAGE_FILE_PATH % (i,), 'wb') as f:
                f.write(requests.get(single_captcha_element_url).content)
            resized_single_captcha_base64_string = resize_base64_image(
                CAPTCHA_SINGLE_IMAGE_FILE_PATH % (i,), (100, 100))
            resized_single_captcha_base64_strings.append(
                resized_single_captcha_base64_string)

        logger.debug(
            f'length of single_captcha_element_urls {len(resized_single_captcha_base64_strings)}')

        # try to verify using API    #发包
        captcha_recognize_result = self.captcha_resolver.create_task(
            resized_single_captcha_base64_strings,
            self.captcha_target_text
        )
        if not captcha_recognize_result:
            logger.error('count not get captcha recognize result')
            return
        recognized_results = captcha_recognize_result.get(
            'solution', {}).get('objects')

        if not recognized_results:
            logger.error('count not get captcha recognized indices')
            return
        # click captchas
        recognized_indices = [i for i, x in enumerate(recognized_results) if x]
        logger.debug(f'recognized_indices {recognized_indices}')
        click_targets = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '.task-image')))
        for recognized_index in recognized_indices:
            click_target: WebElement = click_targets[recognized_index]
            click_target.click()
            time.sleep(rdm())

        # after all captcha clicked
        verify_button: WebElement = self.get_verify_button()
        if verify_button.is_displayed:
            verify_button.click()
            time.sleep(3)

        # check if succeed
        is_succeed = self.get_is_successful()
        if is_succeed:
            logger.debug('verifed successfully')
        else:
            self.verify_captcha()

    def resolve(self):
        self.trigger_captcha()  #2 获取验证码
        self.verify_captcha()  # 发送验证码包
