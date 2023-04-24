import os
import sys
import threading
import time

from serverChan import ServerChan
from userData import user_data
from yiban import Yiban

def start_sign(user: dict):
    server_chan = ServerChan('易班签到详情', user['SendKey'])
    yb = Yiban(user['Phone'], user['PassWord'])
    time_range=yb.task_feedback.get_sign_task()
    while not time_range['StartTime'] < time.time() < time_range['EndTime']:
        time.sleep(1)
    back = yb.submit_sign_feedback(user['Address'])
    server_chan.log(f'{user["Phone"]: {back}}')
    server_chan.send_msg()


DEBUG = True if sys.gettrace() else False

if __name__ == '__main__':
    env = os.getenv('skip')
    if env is not None:
        env = env.split(',')
    else:
        env = ''

    for user in user_data:
        if user['Phone'] in env:
            print(f'用户 {user["Phone"]} 在跳过列表')
            continue

        if DEBUG:
            start_sign(user)
        else:
            threading.Thread(target=start_sign, args=(user,)).start()
