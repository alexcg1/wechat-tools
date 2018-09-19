import itchat

def login():
	import itchat
	print("Logging in")
	itchat.auto_login(enableCmdQR=2, hotReload=True)

def get_friends_and_rooms():
	import itchat

	friends = itchat.get_friends()
	rooms = itchat.get_chatrooms()

	print("Merging friends list and rooms list")
	friends = friends+rooms

	for i in friends:
		# Unify name database
		if i['RemarkName']:
			i['Name'] = i['RemarkName'] # RemarkName is the custom name you can give your friend
		else:
			i['Name'] = i['NickName'] # NickName is the name they choose for themselves

		i['counter'] = 0

	return friends

def chooser(target, friendlist):
	counter = 1
	shortlist = []

	for i in friendlist:
		if target.lower() in i['Name'].lower():
			i['counter'] = counter
			counter += 1
			shortlist.append(i)

	if len(shortlist) == 0:
		print("Error: No such users found")
		exit()

	elif len(shortlist) == 1:
		recipient = shortlist[0]['UserName']
		recipient_name = shortlist[0]['Name']

	else:
		print(len(shortlist), "users in the list")
		print("Please select a user:")

		for i in shortlist:
			print(i['counter'], i['Name'])

		prompt = int(input('> '))

		for i in shortlist:
			if i['counter'] == prompt:
				# print('Recipient will be', i['Name'])
				recipient = i['UserName']
				recipient_name = i['Name']
			# else:
			# 	print("Error: I expected a number")
			# 	exit()

	return (recipient, recipient_name)

def give_name(item):
	class bcolors:
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'
	
	if item['User']['RemarkName']:
		item['User']['Name'] = item['User']['RemarkName']
	else:
		item['User']['Name'] = item['User']['NickName']

	item['User']['FormattedName'] = bcolors.OKGREEN+item['User']['Name']+bcolors.ENDC

	# if item.type == "Text":
	# 	print(bcolors.OKGREEN+item['User']['Name']+bcolors.ENDC+": "+item.text)
	# else:
	# 	print(bcolors.OKGREEN+item['User']['NickName']+bcolors.ENDC+": ["+item.type+"]")

	return item