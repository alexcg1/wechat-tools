import itchat
import os, sys
from colorama import Fore, Back, Style
import pyperclip
import notify2
from pprint import pprint
from datetime import datetime

# def chooser(target, friendlist):
# 	counter = 1
# 	shortlist = []

# 	for i in friendlist:
# 		if target.lower() in i['Name'].lower():
# 			i['counter'] = counter
# 			counter += 1
# 			shortlist.append(i)

# 	if len(shortlist) == 1:
# 		recipient = shortlist[0]['UserName']
# 		recipient_name = shortlist[0]['Name']

# 	elif len(shortlist) > 1:
# 		print(len(shortlist), "users in the list")
# 		print("Please select a user:")

# 		for i in shortlist:
# 			print(i['counter'], i['Name'])

# 		prompt = int(input('Please choose a user > '))

# 		for i in shortlist:
# 			if i['counter'] == prompt:
# 				recipient = i['UserName']
# 				recipient_name = i['Name']

# 	if "recipient" in locals() and "recipient_name" in locals():
# 		return (recipient, recipient_name)
# 	else:
# 		print(Err.user_not_found)

# def give_name(item):
	
# 	if item['User']['RemarkName']:
# 		item['User']['Name'] = item['User']['RemarkName']
# 	else:
# 		item['User']['Name'] = item['User']['NickName']

# 	item['User']['FormattedName'] = Fore.GREEN+item['User']['Name']+Style.RESET_ALL

# 	return item

def unify_names(list):
	for i in list:
	# Unify name database
		if i['RemarkName']:
			i['Name'] = i['RemarkName'] # RemarkName is the custom name you can give your friend
		else:
			i['Name'] = i['NickName'] # NickName is the name they choose for themselves

		i['counter'] = 0
	return list

def download_files(msg, download_dir):
	import os
	os.chdir(download_dir)
	msg.download(msg.fileName)

class App:
	def start():
		notify2.init('WeChatter') # Initialize notifications
		global download_dir
		download_dir = os.getenv("HOME")+'/Downloads/wechat'

	def quit():
		print("Quitting")
		sys.exit()

	def vars():
		print("== GLOBALS ==\n"+globals())
		print("== LOCALS ==\n"+locals())

	def listen():
		itchat.run(debug=False)
		# itchat.run(debug=True)

class Account:
	def login():
		print("Logging in")
		itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='/tmp/itchat.pkl')
		# print("Using WeChat as"+Fore.BLUE,me['NickName'],me['UserName'])
		# print(Style.RESET_ALL) 

	def get_friends():
		friends = itchat.get_friends()
		friends = unify_names(friends)
		return friends

	def friends_and_rooms():
		friends = Account.get_friends() + Account.get_rooms()
		return friends

	def get_rooms():
		rooms = itchat.get_chatrooms()
		rooms = unify_names(rooms)
		return rooms

class Command:
	def download_files(msg, download_dir):
		download_dir = os.getenv("HOME")+'/Downloads/wechat'
		os.chdir(download_dir)
		msg.download(msg.fileName)

class Message:
	def notify(user, message):
		n = notify2.Notification(user, message)
		n.show()

	def copy(msg):
		try:	
			pyperclip.copy(msg)
			print("Message copied")
		except:
			print(Err.no_msg)

	def paste(text, recipient):
		if 'recipient' != '':
			itchat.send_msg(msg=pyperclip.paste(), toUserName=recipient)
		else:
			print(Err.no_recipient)

	# def print(msg):
	# 	pprint(msg)

	def get_sender_human(msg, friendlist):
		FromUser = {}
		FromUser['UserName'] = msg['FromUserName']
		for i in friendlist:
			if i['UserName'] == msg['FromUserName']:
				FromUser['Name'] = i['Name']

		return FromUser

	def translate(text):
		from os import environ
		API_KEY = "Google_API.json"
		environ["GOOGLE_APPLICATION_CREDENTIALS"] = API_KEY
		from google.cloud import translate
		target = 'en'
		translate_client = translate.Client()
		print(translate_client.translate(text, target_language=target))
		# print(Message.translation)



	date_human = datetime.now().strftime('%H:%M:%S')
	separator = 78*"-"

class File:
	def download():
		pass
		download_dir = os.getenv("HOME")+'/Downloads/wechat'
		os.chdir(download_dir)
		msg.download(msg.fileName)

	def send(filename, recipient):
		message = itchat.send_file(filename, toUserName=recipient)
		pass

	def open(filename):
		try:
			print("Opening", last_file)
			os.system('/usr/bin/xdg-open'+' '+download_dir+'/'+filename)
		except:
			print(Err.file_not_found)

	download_dir = os.getenv("HOME")+'/Downloads/wechat'

class Contact:
	def give_name(item):
	
		if item['User']['RemarkName']:
			item['User']['Name'] = item['User']['RemarkName']
		else:
			item['User']['Name'] = item['User']['NickName']

		item['User']['FormattedName'] = Fore.GREEN+item['User']['Name']+Style.RESET_ALL

		return item

	def chooser(target, friendlist):
		counter = 1
		shortlist = []

		for i in friendlist:
			if target.lower() in i['Name'].lower():
				i['counter'] = counter
				counter += 1
				shortlist.append(i)

		if len(shortlist) == 1:
			recipient = shortlist[0]['UserName']
			recipient_name = shortlist[0]['Name']

		elif len(shortlist) > 1:
			text = len(shortlist) + " users in the list:"
			# output_widget.set_text(output_widget.text + "\n" + len(shortlist) + " users in the list:\n")
			# print(len(shortlist), "users in the list")
			# print("Please select a user:")

			for i in shortlist:
				# text = text+"\n"+ i['counter'], i['Name']
				print(i['counter'], i['Name'])

			prompt = int(input('Please choose a user > '))

			for i in shortlist:
				if i['counter'] == prompt:
					recipient = i['UserName']
					recipient_name = i['Name']

		if "recipient" in locals() and "recipient_name" in locals():
			return (recipient, recipient_name)
		else:
			print(Err.user_not_found)

class Err:
	error_base = Fore.RED+"Error: "+Style.RESET_ALL
	no_recipient = error_base+"Please choose a recipient by using the contact command"
	no_msg = error_base+"There's no message to copy text from"
	unrecognized_command = error_base+"Command not recognized"
	file_not_found = error_base+"Having a problem processing that file. Perhaps there are special characters in the filename?"
	user_not_found = error_base+"User not found"
	vidpic_issue = error_base+"Currently video and pic download is glitchy. No promises it'll work!"

class Debug:
	def userstack():
		print(msg_show.from_username_stack)