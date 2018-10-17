#!/usr/bin/env python3

import npyscreen

class FormObject(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name='First name', value="Joe")
		self.add(npyscreen.TitleText, name='Last name', values="Joe")

	def afterEditing(self):
		self.parentApp.setNextForm(None)

class App(npyscreen.NPSAppManaged):
	def onStart(self):
		self.addForm('MAIN', FormObject, name='WeChatter')

if (__name__ == '__main__'):
	app = App().run()