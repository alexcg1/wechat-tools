#!/usr/bin/env python3

import itchat
from itchat.content import *
from wem_functions import *
from pprint import pprint

login()

friends = get_friends_and_rooms()

me = friends[0]

print("Using WeChat as",me['NickName'])


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def msg_show(msg):

	msg = give_name(msg)

	if msg.type == "Text":
		# print(bcolors.OKGREEN+msg['User']['Name']+bcolors.ENDC+": "+msg.text)
		print(msg['User']['FormattedName']+": "+msg.text)

	else:
		print(msg['User']['FormattedName']+": ["+msg.type+"]")

	prompt = input("> ")

	# pprint(msg)
	# print(msg.OriContent) # At least for locations, this pulls in XML giving details

# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def msg_foo(msg):
# 	# print(msg['User']['NickName']+": "+msg.type+" "+msg.text)
# 	print(msg['User']['NickName']+": "+msg.type)



	# os.chdir('/home/alexcg/Downloads/wechat')
	# msg.download(msg.fileName)
	# typeSymbol = {
	# 	PICTURE: 'img',
	# 	VIDEO: 'vid', }.get(msg.type, 'fil')
	# return '@%s@%s' % (typeSymbol, msg.fileName)
	# print("Downloaded"+msg.fileName+"to download folder")

	# with open(msg.fileName, 'wb') as f:
	# 	f.write(msg.download())

	# print(msg['Content'])
	# msg.download()

# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     msg.user.verify()
#     msg.user.send('Nice to meet you!')

# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     if msg.isAt:
#         msg.user.send(u'@%s\u2005I received: %s' % (
#             msg.actualNickName, msg.text))
itchat.run(True)

# prompt = input("> ")

commands = ['help', 'contact', 'quit', 'search']
command_prefix = '\\'

for i in commands:
	if prompt == command_prefix+i:
		print("foo!")