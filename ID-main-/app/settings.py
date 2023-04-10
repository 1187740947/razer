from environs import Env

env = Env()
env.read_env()

CAPTCHA_RESOLVER_API_URL = 'https://api.yescaptcha.com/createTask'  # 验证码api
CAPTCHA_RESOLVER_API_KEY = env.str('CAPTCHA_RESOLVER_API_KEY')      # 密钥

CAPTCHA_DEMO_URL = 'https://razerid.razer.com/new'       # 注册地址pai
MONEY_URL ='https://gold.razer.com/hk/zh-hk'   #钱包地址
EMAIL_URL = 'http://mail.ttwsf.cn/'   #邮箱地址

NAME_EMAIL ='d96306qa28@ttwsf.cn'
PASSWORD = '19zmip2i'

CAPTCHA_ENTIRE_IMAGE_FILE_PATH = 'captcha_entire_image.png'
CAPTCHA_SINGLE_IMAGE_FILE_PATH = 'captcha_single_image_%s.png'
CAPTCHA_RESIZED_IMAGE_FILE_PATH = 'captcha_resized_image.png'
