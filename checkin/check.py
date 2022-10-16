import os
import sys
import requests
import datetime
import json
import hashlib
import random
import string
import time
from urllib.parse import urlencode

try:
    COOKIE_YuanShen = sys.argv[1]  # 根据参数获取cookie
except IndexError:
    project_path = os.path.dirname(__file__)
    cookie_file = os.path.join(project_path, 'checkin', 'COOKIE')
    print(f"cookie 参数获取失败，尝试读取文件:{cookie_file}")
    with open(cookie_file, mode='r', encoding='utf-8') as fr:
        COOKIE_YuanShen = fr.read().strip()

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.36.1'
roles_info_url = "https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn"  # 原神游戏id: game_biz=hk4e_cn
rewards_info_url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id=e202009291139501'  # 原神每月签到奖励信息
sign_info_url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?act_id=e202009291139501&uid={}&region={}'
sign_url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign'  # 签到url


def cookie_to_dict(cookie):
    if cookie and '=' in cookie:
        cookie = dict([line.strip().split('=', 1) for line in cookie.split(';')])
    return cookie


def request(*args, **kwargs):
    is_retry = True  # 是否需要重试标记
    count = 0  # request 次数
    max_retries = 3  # request 重试次数
    sleep_seconds = 5  # request 重试间隔时间
    while is_retry and count <= max_retries:
        try:
            s = requests.Session()
            response = s.request(*args, **kwargs)
            is_retry = False
        except Exception as e:
            if count == max_retries:
                raise e
            print('网络请求失败: {}'.format(e))
            count += 1
            print('重试重新请求 {} seconds ({}/{})...'.format(sleep_seconds, count, max_retries))
            time.sleep(sleep_seconds)
        else:
            return response


def _hexdigest(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def get_ds(ds_type: str = None, new_ds: bool = False, data: dict = None, params: dict = None):
    # 1:  ios
    # 2:  android
    # 4:  pc web
    # 5:  mobile web
    def new():
        t = str(int(time.time()))
        r = str(random.randint(100001, 200000))
        b = json.dumps(data) if data else ''
        q = urlencode(params) if params else ''
        c = _hexdigest(f'salt={salt}&t={t}&r={r}&b={b}&q={q}')
        return f'{t},{r},{c}'

    def old():
        t = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = _hexdigest(f'salt={salt}&t={t}&r={r}')
        return f'{t},{r},{c}'

    app_version = '2.36.1'
    client_type = '5'
    salt = 'YVEIkzDFNHLeKXLxzqCA9TzxCpWwbIbk'
    ds = old()
    if ds_type == '2' or ds_type == 'android':
        app_version = '2.36.1'
        client_type = '2'
        salt = 'n0KjuIrKgLHh08LWSCYP0WXlVXaYvV64'
        ds = old()
    if ds_type == 'android_new':
        app_version = '2.36.1'
        client_type = '2'
        salt = 't0qEgfub6cvueAPgR5m9aQWWVciEer7v'
        ds = new()
    if new_ds:
        app_version = '2.36.1'
        client_type = '5'
        salt = 'xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs'
        ds = new()

    return app_version, client_type, ds


wait_sec = random.randint(0, 60)
print(f"Sleep for {wait_sec} seconds...")
time.sleep(wait_sec)  # 随机睡眠1分钟
cookies = cookie_to_dict(COOKIE_YuanShen)
headers = {'User-Agent': User_Agent}

print("*" * 20, end="")
print('获取角色信息', end="")
print("*" * 20)
response_roles_info = request('get', roles_info_url, headers=headers, cookies=cookies).json()
role_data = response_roles_info['data']['list'][0]
game_uid = role_data['game_uid']
region = role_data['region']
print(f"UID:{game_uid}")
print(f"{role_data['nickname']}  {role_data['level']}  {role_data['region_name']}")

# =======获取签到奖励信息========
print("*" * 20, end="")
print('获取签到奖励信息', end="")
print("*" * 20)
response_rewards_info: dict = request('get', rewards_info_url).json()
index_today_rewards = int(datetime.datetime.today().day) - 1
rewards_today = response_rewards_info['data']['awards'][index_today_rewards]
print(f"今日签到奖励:{rewards_today['name']} x{rewards_today['cnt']}")

# =======获取签到状态========
print("*" * 20, end="")
print('获取签到状态', end="")
print("*" * 20)
sign_info_url = sign_info_url.format(game_uid, region)
response_sign_info = request('get', sign_info_url, headers=headers, cookies=cookies).json()
is_sign = response_sign_info["data"]["is_sign"]
total_sign_day = response_sign_info["data"]["total_sign_day"]
print(f'本月已签到 {total_sign_day} 天.')
if is_sign:
    print("亲爱的旅行者，今日已经签到过了哦！")
    exit(0)

# =======签到========
print("*" * 20, end="")
print('签到', end="")
print("*" * 20)

app_version, client_type, ds = get_ds()
headers['x-rpc-device_id'] = 'B45096D42D953C60AA7C58F0E579CF60'
headers['x-rpc-client_type'] = client_type
headers['x-rpc-app_version'] = app_version
headers['DS'] = ds  # 这个是一个变量！！！
payload = {'act_id': 'e202009291139501', 'region': region, 'uid': game_uid}
response_sign = request('post', sign_url,
                        headers=headers, json=payload,
                        cookies=cookies).json()

print(response_sign['message'])
