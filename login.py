from bilibili import bilibili
from printer import Printer
import numpy as np
import string
import base64
import configloader
import requests


class login():
    auto_captcha_times = 3
    def normal_login(self, username, password):
       
        url = "https://passport.bilibili.com/api/v2/oauth2/login"
        temp_params = 'appkey=' + bilibili().dic_bilibili['appkey'] + '&password=' + password + '&username=' + username
        sign = bilibili().calc_sign(temp_params)
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = "appkey=" + bilibili().dic_bilibili[
            'appkey'] + "&password=" + password + "&username=" + username + "&sign=" + sign
        response = requests.post(url, data=payload, headers=headers)
        return response

    def login_with_captcha(self, username, password):
        cookie_id = ''.join(np.random.choice(list(string.ascii_lowercase + string.digits), 8))
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'Host': 'passport.bilibili.com',
            #'cookie': "sid=hxt5szbb"
            'cookie': "sid=" + cookie_id 
        }
        s = requests.session()
        url = "https://passport.bilibili.com/captcha"
        res = s.get(url, headers=headers)
        tmp1 = base64.b64encode(res.content)
        for _ in range(login.auto_captcha_times):
            try:
                captcha = bilibili().cnn_captcha(tmp1)
                break
            except Exception:
                Printer().printer("验证码识别服务器连接失败","Error","red")
                login.auto_captcha_times -= 1
        else:
            try:
                from PIL import Image
                from io import BytesIO
                img = Image.open(BytesIO(res.content))
                img.show()
                captcha = input('输入验证码\n').strip()
            except ImportError:
                Printer().printer("安装 Pillow 库后重启，以弹出验证码图片","Error","red")
        temp_params = 'actionKey=' + bilibili().dic_bilibili[
            'actionKey'] + '&appkey=' + bilibili().dic_bilibili['appkey'] + '&build=' + bilibili().dic_bilibili[
                          'build'] + '&captcha=' + captcha + '&device=' + bilibili().dic_bilibili[
                          'device'] + '&mobi_app=' + \
                      bilibili().dic_bilibili['mobi_app'] + '&password=' + password + '&platform=' + \
                      bilibili().dic_bilibili[
                          'platform'] + '&username=' + username
        sign = bilibili().calc_sign(temp_params)
        payload = temp_params + '&sign=' + sign
        headers['Content-type'] = "application/x-www-form-urlencoded"
        #headers['cookie'] = "sid=hxt5szbb"
        headers['cookie'] = "sid=" + cookie_id 
        url = "https://passport.bilibili.com/api/v2/oauth2/login"
        response = s.post(url, data=payload, headers=headers)
        return response

    def login(self):
        username = str(bilibili().dic_bilibili['account']['username'])
        password = str(bilibili().dic_bilibili['account']['password'])
        if username != "":
            while True:
                response = bilibili().request_getkey()
                value = response.json()['data']
                key = value['key']
                Hash = str(value['hash'])
                username, password = bilibili().calc_name_passw(key, Hash, username, password)
                response = self.normal_login(username, password)
                while response.json()['code'] == -105:
                    response = self.login_with_captcha(username, password)
                if response.json()['code'] == -662: # "can't decrypt rsa password~"
                    Printer().printer("打码时间太长key失效，重试", "Error", "red")
                    continue
                break
            try:
                access_key = response.json()['data']['token_info']['access_token']
                cookie = (response.json()['data']['cookie_info']['cookies'])
                cookie_format = ""
                for i in range(0, len(cookie)):
                    cookie_format = cookie_format + cookie[i]['name'] + "=" + cookie[i]['value'] + ";"
                bilibili().dic_bilibili['csrf'] = cookie[0]['value']
                bilibili().dic_bilibili['access_key'] = access_key
                bilibili().dic_bilibili['cookie'] = cookie_format
                bilibili().dic_bilibili['uid'] = cookie[1]['value']
                bilibili().dic_bilibili['pcheaders']['cookie'] = cookie_format
                bilibili().dic_bilibili['appheaders']['cookie'] = cookie_format
                dic_saved_session = {
                    'csrf': cookie[0]['value'],
                    'access_key': access_key,
                    'cookie': cookie_format,
                    'uid': cookie[1]['value']
                }
                configloader.write2bilibili(dic_saved_session)
                Printer().printer(f"登录成功", "Info","green")
            except:
                Printer().printer(f"登录失败,错误信息为:{response.json()}","Error","red")

    async def login_new(self):
        if bilibili().dic_bilibili['saved-session']['cookie']:
            Printer().printer(f"复用cookie","Info","green")
            bilibili().load_session(bilibili().dic_bilibili['saved-session'])
        else:
            return self.login()
