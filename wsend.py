#!/usr/bin/env python3

import itchat
import argparse
import io

parser = argparse.ArgumentParser(description="Copy files to Wechat user")
parser.add_argument("file")
parser.add_argument("user")
args = parser.parse_args()

# Check file exists
try:
	fh = open(args.file, 'r')
	# print("File exists!")
except FileNotFoundError:
	print(args.file+": File not found")
	exit()

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

# for i in friends[0:10]:
# 	print(i['Name'],i['UserName'])

# itchat.send_file('functions.py', toUserName='@c19adbeb56a71dd1cfe4479d9f079053b72054f05322e3956193c8e04a09be5e')

# for i in friends:
# 	if args.user == i['Name']:
# 		print("Sending file to",i['Name'], i['UserName'])
# 		itchat.send_file('functions.py', toUserName=i['UserName'])
# 		file_send = itchat.send_file(args.file, toUserName=i['UserName'])

counter = 1
shortlist = []

for i in friends:
	if args.user.lower() in i['Name'].lower():
		i['counter'] = counter
		counter += 1
		shortlist.append(i)

# print(shortlist)


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

print(itchat.send_file(args.file, toUserName=recipient))