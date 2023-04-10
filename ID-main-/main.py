
from app.settings import CAPTCHA_DEMO_URL
from app.solution import Solution
from app.ID_login_spider import Spider_login   # 注册ID
from app.get_email import Verify_Email  # 邮箱验证
from app.money_packg import Mone_pak
from app.settings import EMAIL_URL
from app.settings import MONEY_URL


if __name__ == '__main__':
    Spider_login(CAPTCHA_DEMO_URL).spider()   # 注册账号密码
    Verify_Email(EMAIL_URL).run()            # 验证邮箱
    # Solution(CAPTCHA_DEMO_URL).resolve()  #1   #测试检测验证码
    Mone_pak(MONEY_URL).run()   # 创建钱包