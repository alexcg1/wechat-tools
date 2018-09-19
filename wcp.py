#!/usr/bin/env python3

import itchat
import argparse
import io
from wem_functions import *

parser = argparse.ArgumentParser(description="Send file to Wechat users")
parser.add_argument("file")
parser.add_argument("user")
args = parser.parse_args()

login()

# print("Logging in")
# itchat.auto_login(enableCmdQR=2, hotReload=True)

friends = get_friends_and_rooms()

recipient_info = chooser(args.user, friends)
recipient = recipient_info[0]
recipient_name = recipient_info[1]

print("Sending",args.file, "to", recipient_name,"("+recipient+")")

print(itchat.send_file(args.file, toUserName=recipient))