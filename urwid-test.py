import urwid
import itchat
from wem_functions import *
from pprint import pprint

login()

friends = get_friends()
rooms = get_rooms()

# pprint(friends[-3])

# exit()

friendlist = []
roomlist = []

for i in friends:
    friendlist.append(i['Name'])

for i in rooms:
    roomlist.append(i['Name'])


choices = roomlist
# u'Chapman Cleese Gilliam Idle Jones Palin'.split()

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()

def send_msg(button)

main = urwid.Padding(menu(u'Pythons', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='left', width=('relative', 60),
    valign='top', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()