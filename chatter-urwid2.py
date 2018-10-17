#!/usr/bin/env python3

# import subprocess
import urwid
import os, sys
import pyperclip
import notify2
from datetime import datetime
import pyperclip
import readline
import threading
import time
import itchat
from datetime import datetime
from itchat.content import *
from wem_functions import * # My custom functions
import asyncio # Allows realtime updates instead of on keypress
# from collections import OrderedDict # To remove dups from userstack while maintaining order

# Debugging
# from time import sleep
#from pprint import pprint
#from colorama import Fore, Back, Style 

App.start()
Account.login()

def test_func(text):
	Output.update(text)

command_char = "\\"
friends = Account.friends_and_rooms()
me = friends[0]
global recipient
recipient = {}
global userstack
userstack = [] # Stack of users who have been contacted recently
global message


# global stack_buttons
# stack_buttons = []
# button1 = urwid.Button('Bar')
# urwid.connect_signal(button1, 'click', Output.update, "Bar") # Testing if it works
# button2 = urwid.Button('Foo')
# urwid.connect_signal(button2, 'click', test_func, "Foo") # Testing if it works
# stack_buttons.insert(0, button1)
# stack_buttons.insert(0, button2)

palette = [
		# ('body','white','black'),
		('sidebar', 'white', 'dark gray'),
		('edit', 'black', 'light gray'),
		('header', 'white', 'dark green'),
		('popbg', 'white', 'dark blue')
		]

class MainWindow(urwid.PopUpLauncher):

	def __init__(self):
		# global stack_buttons
		self.output_widget = urwid.Text('')
		self.output_wrapper = urwid.Padding(self.output_widget, left=2, right=2)
		self.edit_widget = urwid.AttrWrap(urwid.Edit(me['NickName']+": "), 'edit')
		self.sidebar_content = urwid.Text("== Recent Contacts ==\n", align='center')
		self.sidebar = urwid.AttrWrap(urwid.Padding(self.sidebar_content, left=2, right=2), 'sidebar') # Implement later - will hold user stack and indicate new msgs
		# self.sidebar_contacts = urwid.AttrWrap(urwid.Text("== Recent Contacts ==\n\n"), 'sidebar') # Implement later - will hold user stack and indicate new msgs
		# self.sidebar_stack = urwid.AttrWrap(urwid.Text("== Recent Contacts ==\n\n"), 'sidebar')
		self.header_text_orig = "WeChatter"
		self.header_text = urwid.Text(self.header_text_orig)
		self.header_widget = urwid.AttrWrap(self.header_text, 'header')

		# self.sidebar = urwid.Pile([urwid.Text("== Recent Users ==\n"), *stack_buttons])
		# self.sidebar = urwid.Pile([*stack_buttons])

		self.main_widget = urwid.Columns([self.output_widget, (40, self.sidebar)])

		self.frame_widget = urwid.Frame(
			header = self.header_widget,
			footer = self.edit_widget,
			body = urwid.Filler(self.main_widget, valign='bottom', min_height=20),
			focus_part = 'footer')

		self.__super.__init__(self.frame_widget)

	def process_text(self, text):
		'''Process whatever was typed into the edit box'''
		if text.startswith(command_char):
			self.process_command(text)
		elif recipient == {}:
			Output.update("Error: No recipient. Please choose someone using the "+command_char+"contact command")
		else:
			msg_text = self.edit_widget.edit_text
			self.send_message(msg_text, recipient)

	def send_message(self, text, user):
		time = datetime.now().strftime('%H:%M:%S')
		msg_prefix = time + ": " + me['NickName'] + ": "
		msg_text = self.edit_widget.edit_text
		itchat.send_msg(msg=text, toUserName=user['UserName'])
		Output.update(msg_prefix + msg_text)
		Sidebar.update(user['CustomName'])
		Stack.add(user)

	def process_command(self, text):
		command = text[1:].lower()

		if command in ['q', 'quit']:
			sys.exit()
		elif command.startswith("contact"):
			search_string = command[8:]
			self.contact_chooser(search_string)
		elif command in ['stack']:
			for i in userstack:
				self.update_output(i['UserName']+" "+i['NickName'])
		elif command in ['yy', 'copy']:
			pyperclip.copy(message.text)
		elif command in ['pp', 'paste']:
			self.send_message(pyperclip.paste(), recipient)
		else:
			Output.update('Command not recognized')

	def contact_chooser(self, search_string):
		global user_shortlist
		user_shortlist = []
		for i in friends:
			if search_string in i['CustomName'].lower():
				user_shortlist.append(i)
		self.open_pop_up()

	def update_output(self, text):
		self.output_widget.set_text(self.output_widget.text + "\n" + text)

	def update_sidebar(self, text):
		self.sidebar.set_text(self.sidebar.text + "\n" + text)

	def output_update(dsfs, self, text):
		'''Deprecated - but contact chooser still relies on it'''
		program.output_widget.set_text(program.output_widget.text + "\n" + text)

	def confirm_user(dsfs, self, user):
		'''What happens after selecting a user in the chooser'''
		global recipient
		recipient = user
		program.edit_widget.set_caption("To: "+user['CustomName']+": ")
		program.header_text.set_text(program.header_text_orig + " " + user['CustomName'])
		Stack.add(user)
		program.close_pop_up()
		return user

	def key_input(self, key):
		if key == 'enter':
			self.process_text(self.edit_widget.edit_text)
			self.edit_widget.set_edit_text("") # Clear edit box
		elif key == 'ctrl d':
			sys.exit()
		elif key == 'ctrl s':
			self.sidebar.set_focus(1)
		elif key == 'esc':
			self.close_pop_up()
			self.frame_widget.set_focus('footer')

	def create_pop_up(self):
		pop_up = PopUpDialog()
		urwid.connect_signal(pop_up, 'close',
			lambda button: self.close_pop_up())
		return pop_up

	def get_pop_up_parameters(self):
		return {'left':15, 'top':5, 'overlay_width':60, 'overlay_height':30}

program = MainWindow()

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def msg_show(msg):
	'''What to do when a new message comes in'''
	global message
	FromUser = Message.get_sender_human(msg, friends)
	Message.indicator = Message.date_human+": "+FromUser['Name']+": "

	msg.from_name = FromUser['Name']
	msg.from_username = msg.FromUserName
	msg.prefix = Message.date_human + ": " + msg.from_name + ": "
	# msg.display = msg.prefix + msg.text

	# if msg.FromUserName != me.UserName:
	# 	msg_show.from_username_stack.append(msg.FromUserName)

	if msg.type == "Text":
		# Message.display_text = msg.text
		# Message.display_text = Message.indicator+msg.text
		msg.display = msg.prefix + msg.text
		msg.notification = msg.text
	elif msg.type in ['Attachment', 'Picture', 'Video']:
		download_files(msg, File.download_dir)
		msg.display = msg.prefix + msg.FileName + "downloaded to " + File.download_dir
		# Message.display_text = Message.indicator+" ["+msg.FileName+"] downloaded to "+File.download_dir
		msg.notification = msg.FileName
		# msg_show.filename = msg.FileName
	else:
		msg.display = msg.prefix + msg.type
		# Message.display_text = Message.indicator+"["+msg.type+"]"
		msg.notify = msg.type

	message = msg
	Output.update(msg.display)
	# Message.notify(msg.from_name, msg.notify)

	# Pull user info into stack for future sidebar use
	this_user = {}
	this_user['UserName'] = msg.from_username
	this_user['NickName'] = msg.from_name
	Stack.add(this_user)
 	

def msg_receiver():
	App.listen()

# def add_user_to_stack(user):
# 	global userstack
# 	userstack.insert(0, user)
	# userstack = list(OrderedDict.fromkeys(userstack))

def set_recipient(user):
	recipient = user['UserName']

def switch_chat_partner(user):
	'''This will select a new chat partner from chat history'''
	pass
	# Select from sidebar
	# Clear output screen
	# Load output screen with prior messages, timestamps
	# Change title of output screen to nickname of new partner
	# Set recipient to new chat partner

# class User(): 
# 	'''We'll add users to the stack here. Later function. How to make instance name == escaped UserName tho?'''
# 	self.UserName = ""
# 	self.NickName = ""
# 	self.msg_history = []
# 	self.update_time = ''
# 	self.new_msg = False

class PopUpDialog(urwid.WidgetWrap):
	signals = ['close']
	def __init__(self):

		buttons = []
		for i in user_shortlist:
			data = [i['NickName'], i['UserName']]
			button = urwid.Button(i['CustomName'])
			urwid.connect_signal(button, 'click', program.confirm_user, i)
			buttons.append(button)

		close_button = urwid.Button("Cancel")
		urwid.connect_signal(close_button, 'click', lambda button:self._emit("close"))
		buttons.append(close_button)

		pile = urwid.Pile([urwid.Text(
			"Select user:\n"), *buttons])

		fill = urwid.Padding(urwid.Filler(pile, valign="middle", height='pack', top=5, bottom=5, min_height=40), left=3, right=3)
		self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))

class Sidebar():
	def wipe():
		program.sidebar_content.set_text('')

	def update(text):
		program.sidebar_content.set_text(program.sidebar_content.text + '\n' + text)

class Output():
	def wipe():
		program.output_widget.set_text('')

	def update(text):
		program.output_widget.set_text(program.output_widget.text + '\n' + text)

class Stack():
	users = []
	buttons = []

	# def __init__(self):
	# 	self.users = []
	# 	self.buttons = []

	def add(user):
		'''Add user to top of stack'''
		global userstack

		if user != me:
			if user in userstack:
				del userstack[userstack.index(user)]
			userstack.insert(0, user)

		# if user in self.users:
		# 	del self.users[self.users.index(user)]
		# self.users.insert(0, user)

	def createButton(user):
		'''Creates a button which sets user as recipient'''
		pass
		button = urwid.Button(user['CustomName'])
		# urwid.connect_signal(button, 'click', program.confirm_user, i)
		urwid.connect_signal(button, 'click', test_func, user['UserName']) # Testing if it works
		Stack.buttons.insert(0, button)

	def show():
		global userstack
		userstack_uniq = []
		text = ''
		for i in userstack:
			if i not in userstack_uniq:
				userstack_uniq.insert(0, i)
			# text = i['NickName']+ '\n' + text
		for i in userstack_uniq:
			text = i['CustomName'] + '\n' + text
		
		return text

# Start loops

msg_thread = threading.Thread(target = msg_receiver)
msg_thread.daemon = True
msg_thread.start()

async_loop = asyncio.get_event_loop()

# UI loop - apparently I shouldn't run in a separate thread
loop = urwid.MainLoop(program, palette=palette, pop_ups=True, unhandled_input=program.key_input, event_loop=urwid.AsyncioEventLoop(loop=async_loop))
loop.run()