#!/usr/bin/env python3

import itchat
from itchat.content import *
import os

download_dir = os.getenv("HOME")+'/Downloads/wechat'

print("WeChat File Listener Daemon started")
print("Files will be downloaded to",download_dir)

itchat.auto_login(True)

# friendlist = itchat.get_friends()
# me = friendlist[0]

# print("Using WeChat as",me['NickName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
	os.chdir('/home/alexcg/Downloads/wechat')
	msg.download(msg.fileName)
	typeSymbol = {
		PICTURE: 'img',
		VIDEO: 'vid', }.get(msg.type, 'fil')
	print("Downloaded \'"+msg.fileName+"\' to "+download_dir)

itchat.run(True)