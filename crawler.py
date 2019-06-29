# -*- coding: UTF-8 -*-

import requests
import json
import itchat
from threading import Timer
import random
import os
import time
import sys

room_status_map = {}


def record(msg):
    log_name = time.strftime("log-%Y-%m-%d.txt", time.localtime())
    if not os.path.exists(sys.path[0] + "/log"):
        os.makedirs(sys.path[0] + "/log")
    log_file = sys.path[0] + "/log/" + log_name
    with open(log_file, "a+") as f:
        print msg
        f.write(msg + "\n")
        f.close()


def search_avail_room():
    # 程序开始
    url = "http://www.998.com/HotelDetail/GetRoomTypeList"

    payload = {'hotelCode': '122529', 'startDate': '2019-08-17', 'endDate': '2019-08-18'}

    ret = requests.post(url, data=payload)

    obj = json.loads(ret.text)

    if "RoomTypeList" in obj.keys():
        rooms = obj["RoomTypeList"]
        for i in range(len(rooms)):
            record("\n第{0}种房型".format(i))
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
            if not room_status_map.has_key(room_name):
                room_status_map[room_name] = False
            last_status = room_status_map[room_name]

            # Check current room available status
            if avail_num > 0:
                current_status = True
                record("有房")
            else:
                current_status = False
                record("无房")
            if current_status != last_status:
                record("状态变化，从{0}到{1}".format(last_status, current_status))

    interval = random.randint(10, 20)
    t = Timer(interval, search_avail_room)
    t.start()


def send_wechat():
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    result = itchat.search_friends(wechatAccount='zhaopengxin1208')

    print result


def main():
    search_avail_room()
    
    
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()


# jstring = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
#
# print jstring
