#!/usr/bin/env python3

import subprocess
import urwid
import itchat
import os, sys
from colorama import Fore, Back, Style
import pyperclip
import notify2
from pprint import pprint
from datetime import datetime
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

App.start()
Account.login()

command_char = "\\"
to_me, from_me = Fore.GREEN, Fore.BLUE
unstyle = Style.RESET_ALL

friends = Account.friends_and_rooms()
me = friends[0]

palette = [
		('body','light gray','black'),
		('edit', 'black', 'light gray'),
		('header', 'white', 'dark green')
		]

# output_widget = urwid.AttrWrap(urwid.Text(""), 'body')
# edit_widget = urwid.AttrWrap(urwid.Edit(me['NickName']+": "), 'edit')
# header_widget = urwid.AttrWrap(urwid.Text("WeChatter"), 'header')
# frame_widget = urwid.Frame(
# 	header = header_widget,
#     footer = edit_widget,
#     body = urwid.Filler(output_widget, valign='bottom'),
#     focus_part = 'footer')

# chooser_body_widget = urwid.Text("Contacts go here!")
# chooser_body_wrapper = urwid.AttrWrap(chooser_body_widget, 'body')
# chooser_edit_widget = urwid.Edit(me['NickName']+": ")
# chooser_edit_wrapper = urwid.AttrWrap(chooser_edit_widget, 'edit')
# chooser_frame = urwid.Frame(body = chooser_body_wrapper, footer = chooser_edit_wrapper)
# chooser_overlay = urwid.Overlay(chooser_frame, frame_widget, align="center", valign="middle", height="pack", width="pack")

# class MainWindow():
class MainWindow(urwid.PopUpLauncher):

	output_widget = urwid.AttrWrap(urwid.Text(""), 'body')
	edit_widget = urwid.AttrWrap(urwid.Edit(me['NickName']+": "), 'edit')
	header_widget = urwid.AttrWrap(urwid.Text("WeChatter"), 'header')
	pop_button = urwid.Button("that's pretty cool")
	urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())
	frame_widget = urwid.Frame(
		header = header_widget,
		footer = edit_widget,
		body = urwid.Filler(pop_button, valign='bottom'),
		focus_part = 'body')

	def __init__(self):
		pass
		self.__super.__init__(self.frame_widget)

	def process_text(text):
		if text.startswith(command_char): 
			command = text[1:].lower()
			if command in ['q', 'quit']:
				sys.exit()
			elif command.startswith("contact "):
				arg = command[8:]
				user_to_contact = Contact.chooser_urwid(arg, friends)
				if user_to_contact != None:
					recipient = user_to_contact[0]
				else:
					del user_to_contact
				self.output_widget.set_text(self.output_widget.text + "\n" + user_to_contact)
			elif command == 'test':
				popup_contact_chooser()
		
		else: 
			self.output_widget.set_text(self.output_widget.text + "\n" + me['NickName']+": " + self.edit_widget.edit_text)

	# def create_pop_up(self):
	# 	pop_up = PopUpDialog()
	# 	urwid.connect_signal(pop_up, 'close',
	# 		lambda button: self.close_pop_up())
	# 	return pop_up

	# def get_pop_up_parameters(self):
	# 	return {'left':0, 'top':1, 'overlay_width':32, 'overlay_height':7}

	def contacter(self):
		content = urwid.Text("Foo")
		# question = urwid.Text(("bold", "Really quit?"), "center")
		# yes_btn = urwid.AttrMap(urwid.Button(
		# 	"Yes", self.button_press, "quit"), "red", None)
		# no_btn = urwid.AttrMap(urwid.Button(
		# 	"No", self.button_press, "back"), "green", None)

		# prompt = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(
		# 	[question, self.div, self.div, no_btn, yes_btn])))

		# The only interesting thing in this method is this Overlay widget.
		overlay = urwid.Overlay(
			content, self.loop.baseWidget,
			"center", 20, "middle", 8,
			16, 8,
			parent=self)
		self.loop.Widget = overlay


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def msg_show(msg):
	FromUser = Message.get_sender_human(msg, friends)
	Message.indicator = Message.date_human+": "+FromUser['Name']+": "
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
		Message.display_text = Message.indicator+" ["+msg.FileName+"] downloaded to "+File.download_dir
		Message.notification_text = msg.FileName
		msg_show.filename = msg.FileName
	else:
		Message.display_text = Message.indicator+"["+msg.type+"]"
		Message.notification_text = msg.type

	MainWindow.output_widget.set_text(MainWindow.output_widget.text + "\n" + Message.display_text)
	# update_output(Message.display_text)


	# try:
	# 	if msg_show.from_username_stack[-1] != msg_show.from_username_stack[-2]:
	# 		print(Message.separator) # Print separator if sender is different to last sender
	# except:
	# 	pass

	Message.notify(FromUser['Name'], Message.notification_text)

def update_output(msg_text):
	output_widget.set_text(output_widget.text + "\n" + msg_text)

def key_input(key):
	if key == 'enter': 
		# MainWindow.open_pop_up()
		process_text(MainWindow.edit_widget.edit_text)
		MainWindow.edit_widget.set_edit_text("") # Clear edit box

def msg_receiver():
	App.listen()

# now threading1 runs regardless of user input
threading1 = threading.Thread(target=msg_receiver)
threading1.daemon = True
threading1.start()

def process_text(text):
	# MainWindow.output_widget.set_text(output_widget.text + "foo")
	if text.startswith('\\'): 
		command = text[1:].lower()

		if command in ['q', 'quit']:
			sys.exit()

		elif command.startswith("contact "):
			arg = command[8:]
			user_to_contact = Contact.chooser_urwid(arg, friends)
			if user_to_contact != None:
				recipient = user_to_contact[0]
			else:
				del user_to_contact
			MainWindow.output_widget.set_text(output_widget.text + "\n" + user_to_contact)
		elif command == 'test':
			contactbox = MainWindow()
			contactbox.contacter()
			# MainWindow.contacter()

	else: 
		MainWindow.output_widget.set_text(MainWindow.output_widget.text + "\n" + me['NickName']+": " + MainWindow.edit_widget.edit_text)

class ChooserDialog(urwid.WidgetWrap):
	"""A dialog that appears with nothing but a close button """
	# signals = ['close', 'foo']

	def __init__(self):
		buttons = []

		for i in friends:
			button = urwid.Button(i['NickName'])
			name = i['NickName']
			username = i['UserName']
			urwid.connect_signal(button, 'click', change_text, [name, username])
			buttons.append(button)


		pile = urwid.Pile([main_text, *buttons])

		fill = urwid.Filler(pile)
		self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))



def received_output(data):
	output_widget.set_text(output_widget.text + data.decode('utf8'))

class PopUpDialog(urwid.WidgetWrap):
	"""A dialog that appears with nothing but a close button """
	signals = ['close']
	def __init__(self):
		close_button = urwid.Button("that's pretty cool")
		urwid.connect_signal(close_button, 'click',
			lambda button:self._emit("close"))
		pile = urwid.Pile([urwid.Text(
			"^^  I'm attached to the widget that opened me. "
			"Try resizing the window!\n"), close_button])
		fill = urwid.Filler(pile)
		self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))

# loop = urwid.MainLoop(frame_widget, palette = palette, unhandled_input=exit_on_enter)
# write_fd = loop.watch_pipe(received_output)

# loop.run()
# proc.kill()

# fill = urwid.Filler(urwid.Padding(MainWindow(), 'center', 15))
# loop = urwid.MainLoop(frame_widget, palette=palette, unhandled_input=exit_on_enter, pop_ups=True)
loop = urwid.MainLoop(MainWindow(), palette =palette, pop_ups=True, unhandled_input=key_input)
loop.run()