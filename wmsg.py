#!/usr/bin/env python3

import itchat
import argparse
import io

parser = argparse.ArgumentParser(description="Send messages to Wechat user")
parser.add_argument("msg")
parser.add_argument("user")
args = parser.parse_args()

print("Logging in")
itchat.auto_login(enableCmdQR=2, hotReload=True)

friends = itchat.get_friends()

for i in friends:
	# Unify name database
	if i['RemarkName']:
		i['Name'] = i['RemarkName'] # RemarkName is the custom name you can give your friend
	else:
		i['Name'] = i['NickName'] # NickName is the name they choose for themselves

	i['counter'] = 0

counter = 1
shortlist = []

for i in friends:
	if args.user.lower() in i['Name'].lower():
		i['counter'] = counter
		counter += 1
		shortlist.append(i)

if len(shortlist) == 0:
	print("Error: No such users found")

elif len(shortlist) == 1:
	recipient = shortlist[0][ 'UserName']
	recipient_name = shortlist[0]['Name']

else:
	print(len(shortlist), "users in the list")
	print("Please select a user:")

	for i in shortlist:
		print(i['counter'], i['Name'])

	prompt = input('> ')
	for i in shortlist:
		if i['counter'] == int(prompt):
			# print('Recipient will be,' i['Name'])
			recipient = i['UserName']
			recipient_name = i['Name']

print("Recipient will be", recipient_name, recipient)

print(itchat.send_msg(msg=args.msg, toUserName=recipient))