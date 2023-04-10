import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from app.solution import Solution
from app.settings import NAME_EMAIL


class Mone_pak(Solution):

    def __init__(self,url):
        super(Mone_pak, self).__init__(url)

    def get_money_url(self):
        time.sleep(3)
        self.browser.find_element(By.CLASS_NAME,'b-dropdown-form').click()
        time.sleep(5)
        # self.browser.switch_to.default_content()
        self.browser.find_element(By.XPATH,'//*[@id="input-login-email"]').send_keys(NAME_EMAIL)
        self.browser.find_element(By.XPATH,'//*[@id="input-login-password"]').send_keys('zydszcdwm123')
        self.browser.find_element(By.ID,'btn-log-in').click()
        time.sleep(5)
        self.browser.find_element(By.ID,'btn-skip').click()   # 跳过
        time.sleep(5)

    def home_lo(self):
        time.sleep(5)
        self.browser.find_element(By.ID,'profile').click()
        time.sleep(5)
        self.browser.find_element(By.XPATH,'//*[@id="profile"]/ul/div/div[2]/a').click()
        time.sleep(5)
        label = self.browser.find_element(By.CSS_SELECTOR, '.custom-control-label')
        self.browser.execute_script('arguments[0].click()', label)
        time.sleep(3)
        self.browser.find_element(By.CSS_SELECTOR,'div.text-center>button').click()
    def run(self):
        # self.get_money_url()
        self.home_lo()

