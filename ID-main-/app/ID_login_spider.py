import string
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from app.solution import Solution
from app.settings import NAME_EMAIL
from app.settings import PASSWORD


class Spider_login(Solution):

    def __init__(self,url):
        super(Spider_login, self).__init__(url)
        self.sol = Solution

    def spider(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[text() = "接受所有 Cookie"]')))
        self.browser.find_element(By.XPATH, '//*[text() = "接受所有 Cookie"]').click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[text() = "我同意"]')))
        self.browser.find_element(By.XPATH, '//*[text() = "我同意"]').click()
        chosen = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, random.randint(9, 14))
        self.browser.find_element(By.XPATH, '//*[@id="input-razerid"]').send_keys("".join(chosen))  # ID
        time.sleep(5)  # 等待ID 校验是否可注册
        ID = self.browser.find_element(By.ID, 'input-razerid').get_attribute("class")
        ID_False = 'error form-control'
        # ID_True = 'form-control'
        while ID is not ID_False:  # 无限修改
            if ID_False in ID:
                self.browser.find_element(By.XPATH, '//*[@id="input-razerid"]').send_keys(
                    random.randint(3, 9))  # ID  修改
                ID = self.browser.find_element(By.ID, 'input-razerid').get_attribute("class")
            else:
                break
        self.browser.find_element(By.XPATH, '//*[@id="react-select-2-input"]').send_keys('中国', Keys.ENTER)  # 国家
        self.browser.find_element(By.XPATH, '//*[@id="input-dob"]').send_keys('02/05/1995')  # 出生年月日
        self.browser.find_element(By.XPATH, '//*[@id="input-signup-email"]').send_keys(NAME_EMAIL)  # 邮箱
        self.browser.find_element(By.XPATH, '//*[@id="input-signup-password"]').send_keys('zydszcdwm123')  # 密码
        self.browser.find_element(By.XPATH,
                                  '//*[@id="login"]/form/div/div[2]/ul/li[2]/label/div[2]/div/span').click()  # 选择优惠券
        self.resolve()  #解析验证码

        self.browser.switch_to.default_content()
        self.browser.find_element(By.XPATH, '//*[@id="btn-start"]').click()  # 点击注册


