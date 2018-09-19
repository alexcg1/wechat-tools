#!/usr/bin/env python3

import itchat, time
import argparse
# import io
from wem_functions import *
from itchat.content import *

# parser = argparse.ArgumentParser(description="Send file to Wechat users")
# parser.add_argument("file")
# parser.add_argument("user")
# args = parser.parse_args()

print("Logging in")
itchat.auto_login(enableCmdQR=2, hotReload=True)

friends = get_friends_and_rooms()

itchat.start_receiving()
itchat.get_msg()