# -*- coding: UTF-8 -*-

import requests
import json
from threading import Timer
import random
import os
import time
import sys
import smtplib
from email.mime.text import MIMEText

room_avail_num_map = {}
iteration_count = 0


def record(msg):
    log_name = time.strftime("log-%Y-%m-%d.txt", time.localtime())
    if not os.path.exists(sys.path[0] + "/log"):
        os.makedirs(sys.path[0] + "/log")
    log_file = sys.path[0] + "/log/" + log_name
    with open(log_file, "a+") as f:
        print msg
        f.write(time.strftime("%Y-%m-%d-%H:%M:%S ", time.localtime()) + msg + "\n")
        f.close()


def alter_me(subject, msg):
    record("发送邮件成功开始")
    record("内容：" + msg)
    msg = time.strftime("%Y-%m-%d-%H:%M:%S ", time.localtime()) + msg
    mailserver = "smtp.126.com"  # 邮箱服务器地址
    username_send = 'zhaopengxin@126.com'  # 邮箱用户名
    password = 'Jim88757167'  # 邮箱密码：需要使用授权码
    username_recv = 'zhaopengxin@126.com'  # 收件人，多个收件人用逗号隔开
    mail = MIMEText(msg, 'plain', 'utf-8')
    mail['Subject'] = subject
    mail['From'] = username_send  # 发件人
    mail['To'] = username_recv  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
    smtp = smtplib.SMTP(mailserver, port=25)  # 连接邮箱服务器，smtp的端口号是25
    smtp.login(username_send, password)  # 登录邮箱
    smtp.sendmail(username_send, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.quit()  # 发送完毕后退出smtp
    record("邮件成功发送")


def search_avail_room():
    global iteration_count
    global room_avail_num_map

    iteration_count = (iteration_count + 1) % 100   # range from [0 - 99]
    if iteration_count == 1:
        alter_me("心跳包", time.strftime("%Y-%m-%d-%H:%M:%S 还活着", time.localtime()))
    record("第{0}次迭代周期开始".format(iteration_count))
    # 程序开始
    url = "http://www.998.com/HotelDetail/GetRoomTypeList"
    payload = {'hotelCode': '122529', 'startDate': '2019-08-17', 'endDate': '2019-08-18'}
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Host': 'www.998.com',
               'Origin': 'http://www.998.com',
               'Referer': 'http://www.998.com/HotelDetail/Index',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    ret = requests.post(url, data=payload, headers=headers)

    obj = json.loads(ret.text)

    if "RoomTypeList" in obj.keys():
        rooms = obj["RoomTypeList"]
        for i in range(len(rooms)):
            record("")
            record("第{0}种房型".format(i))
            room_map = rooms[i]
            if not room_map.has_key("RoomName") or not room_map.has_key("TotalRooms") or not room_map.has_key("AvailRooms"):
                record("Status Error")
                continue
            room_name = room_map["RoomName"]
            total_rooms = int(room_map["TotalRooms"])
            avail_num = int(room_map["AvailRooms"])

            # Print status
            record("Room Name: {0}".format(room_name))
            record("Total Rooms: {0}".format(total_rooms))
            record("Available Rooms: {0}".format(avail_num))

            # Set last status for room
            if not room_avail_num_map.has_key(room_name):
                room_avail_num_map[room_name] = 0
            last_avail_num = room_avail_num_map[room_name]
            room_avail_num_map[room_name] = avail_num

            # Check current room available status
            if avail_num > 0:
                record("有房")
            else:
                record("无房")
            if last_avail_num != avail_num:
                txt = "状态变化，房型{0}状态发生变化，之前房间数{1},目前间数{2}间".format(room_name, last_avail_num, avail_num)
                record(txt)
                alter_me("[提醒] 房型有变化", txt)
    record("第{0}次迭代周期结束\n".format(iteration_count))
    # Set cron job
    interval = random.randint(900, 1800)
    t = Timer(interval, search_avail_room)
    t.start()


def main():
    search_avail_room()
    
    
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()


# jstring = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
#
# print jstring
