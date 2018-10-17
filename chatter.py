#!/usr/bin/env python3

import pyperclip
import readline
import threading
import time
import sys
import os
import itchat
from datetime import datetime
from itchat.content import *
from wem_functions import *
from pprint import pprint
from colorama import Fore, Back, Style 

global chat_partner

App.start()

global output_widget

# download_dir = os.getenv("HOME")+'/Downloads/wechat'
# download_dir = File.download_dir
command_char = "\\"
to_me, from_me = Fore.GREEN, Fore.BLUE
unstyle = Style.RESET_ALL

Account.login()
friends = Account.friends_and_rooms()
me = friends[0]
print("Using WeChat as"+from_me,me['NickName'],me['UserName']+unstyle)
print("Files will be downloaded to",File.download_dir)

# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])

# def msg_show(msg):
# 	print(datetime.now().strftime('%H:%M:%S'+": "), end="", flush=True)
# 	msg = Contact.give_name(msg) # Give a contact name to the message

# 	# pprint(msg)

# 	# Dig out who message was from and assign their human-readable name
# 	FromUser = {}
# 	FromUser['UserName'] = msg['FromUserName']
# 	for i in friends:
# 		if i['UserName'] == msg['FromUserName']:
# 			FromUser['Name'] = i['Name']

# 	# What to do for different message types
# 	if msg.type == "Text":
# 		print(to_me+FromUser['Name']+": "+unstyle+msg.text)

# 		Message.notify(FromUser['Name'],msg.text)

# 	elif msg.type in ['Attachment', 'Picture', 'Video']:
# 		download_files(msg, download_dir)
# 		print(to_me+FromUser['Name']+": "+unstyle+" ["+msg['FileName']+"] "+Style.DIM + "downloaded to "+download_dir+Style.RESET_ALL)
# 		global last_file
# 		last_file = msg['FileName']
# 		MessageStuff['FileName'] = msg['FileName']

# 		Message.notify(FromUser['Name'],"[File] "+msg['FileName'])

# 	else:
# 		print(to_me+FromUser['Name']+": "+unstyle+" ["+msg.type+"]")
	

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])

def msg_show(msg):
	FromUser = Message.get_sender_human(msg, friends)
	Message.indicator = Message.date_human+": "+to_me+FromUser['Name']+": "+unstyle
	msg = Contact.give_name(msg) # Give a contact name to the message

	msg_show.msg_text = msg.text
	msg_show.from_name = FromUser['Name']
	msg_show.from_username = msg.FromUserName
	msg_show.from_username_stack = []

	if msg.FromUserName != me.UserName:
		msg_show.from_username_stack.append(msg.FromUserName)

	if msg.type == "Text":
		Message.display_text = Message.indicator+msg.text
		Message.notification_text = msg.text

	elif msg.type in ['Attachment', 'Picture', 'Video']:
		download_files(msg, File.download_dir)
		Message.display_text = Message.indicator+" ["+msg.FileName+"] "+Style.DIM + "downloaded to "+File.download_dir+unstyle
		Message.notification_text = msg.FileName
		msg_show.filename = msg.FileName

		if msg.type in ['Picture', 'Video']:
			print(Err.vidpic_issue)

	else:
		Message.display_text = Message.indicator+"["+msg.type+"]"
		Message.notification_text = msg.type

	# print(Message.separator)
	print(Message.display_text)

	try:
		if msg_show.from_username_stack[-1] != msg_show.from_username_stack[-2]:
			print(Message.separator) # Print separator if sender is different to last sender
	except:
		pass

	Message.notify(FromUser['Name'], Message.notification_text)

# @itchat.msg_register([ATTACHMENT, PICTURE, VIDEO])
# def msg_show(msg):
# 	msg = Contact.give_name(msg) # Give a contact name to the message
# 	FromUser = Message.get_sender_human(msg, friends)
	
	# if msg.type = 
	# download_files(msg, download_dir)
	# print(to_me+FromUser['Name']+": "+unstyle+" ["+msg['FileName']+"] "+Style.DIM + "downloaded to "+download_dir+Style.RESET_ALL)
	# Message.notify(FromUser['Name'],"[File] "+msg['FileName'])

	# msg_show.msg_text = msg.text
	# msg_show.from_name = FromUser['Name']
	# msg_show.from_username = msg.FromUserName
	# if msg.type in ['Picture', 'Attachment', 'Video']:
	# 	msg_show.filename = msg.FileName

# @itchat.msg_register([MAP, CARD, NOTE, SHARING, RECORDING])
# def msg_show(msg):

def msg_receiver():
	App.listen()

# now threading1 runs regardless of user input
threading1 = threading.Thread(target=msg_receiver)
threading1.daemon = True
threading1.start()

while True:
	if 'user_to_contact' in locals():
		prompt = input(from_me+"To: "+user_to_contact[1]+": "+unstyle)
	else:
		prompt = input("> ")

	if prompt.startswith(command_char):
		command = prompt[1:] # Cuts off the command char, to give us raw command text
		
		if command in ["quit", "q"]:
			App.quit()

		elif command == "open":
			File.open(msg.FileName)

		elif command in ["pp", "paste"]:
			if 'recipient' in locals():
				Message.paste(pyperclip.paste(), recipient)
			else:
				print(Err.no_recipient)

		elif command in ['yy', 'copy']:
			Message.copy(msg_show.msg_text)

		elif command.startswith("contact "):
			arg = prompt[9:]
			user_to_contact = Contact.chooser(arg, friends)
			if user_to_contact != None:
				recipient = user_to_contact[0]
			else:
				del user_to_contact

		elif command in ['translate', 'tr']:
			Message.translate(msg_show.msg_text)

		elif command == "stack":
			print(msg_show.from_username_stack)
			# Debug.userstack()

		elif command.startswith("send "):
			filename = prompt[6:]
			try:
				File.send(filename, recipient)
			except:
				print(Err.no_recipient)		

		else:
			print(Err.unrecognized_command)

	# Now, if there's no command, send a message to selected recipient
	else:
		if 'recipient' in locals():
			message = itchat.send_msg(msg=prompt, toUserName=recipient)
			
			if message['BaseResponse']['RawMsg'] != "请求成功":
				print("Message failed with error:",message['BaseResponse']['ErrMsg'])
			
			# print(me['NickName']+": "+prompt) # For now we still see the prompt above where I typed the message, so disabling for now
		else:
			print(Err.no_recipient)