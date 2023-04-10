import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from app.settings import EMAIL_URL
from app.solution import Solution
from app.settings import NAME_EMAIL
from app.settings import PASSWORD


class Verify_Email(Solution):

    def __init__(self,url):
        super(Verify_Email, self).__init__(url)

    def email_login(self):
        self.browser.find_element(By.XPATH,'//*[@id="rcmloginuser"]').send_keys(NAME_EMAIL)
        self.browser.find_element(By.XPATH,'//*[@id="rcmloginpwd"]').send_keys(PASSWORD)
        self.browser.find_element(By.XPATH,'//*[@id="rcmloginsubmit"]').click()

    def email_cerify(self):
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[text()="RAZER ID：电子邮箱验证"]')))
        self.browser.find_element(By.XPATH,'//*[text()="RAZER ID：电子邮箱验证"]').click()
        time.sleep(5)
        self.browser.switch_to.frame('messagecontframe')  #ID
        self.browser.find_element(By.XPATH, '//*[text()="验证"]').click()
        print('验证完成')
    def run(self):
        self.email_login()
        self.email_cerify()

