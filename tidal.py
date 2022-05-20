import psutil
import win32gui
import win32process
import pypresence
import time
import sys
import os

from datetime import datetime


def pprint(txt): sys.stdout.write(
	f'  \033[1;31m{datetime.now().strftime("%H:%M:%S")} \033[1;30m=> \033[0m\033[38;5;250m{txt}\033[0m' + '\n')


def enum_windows():
	windows = []

	def enum_callback(hwnd, results):
		results.append((hwnd, win32gui.GetWindowText(hwnd), win32process.GetWindowThreadProcessId(hwnd)[1]))

	win32gui.EnumWindows(enum_callback, windows)
	return windows


def find_tidal():
	window = enum_windows()
	for hwnd, title, pid in window:
		try:
			process = psutil.Process(pid)
			if process.name() == "TIDAL.exe":
				if title == "" or title == "Default IME" or title == "MSCTFIME UI":
					continue
				return title
		except:
			pass


os.system("cls")
pprint('Connecting to Discord...')
previous_title = "nun"
presence = pypresence.Presence("944192427860820039")
presence.connect()
pprint('Connected to discord.')
time.sleep(1)
# pprint("Connecting to Tidal...")
# (f"{check_login()}")
time.sleep(2)
os.system("cls")
check = 0

while True:
	tidal_title = find_tidal()
	if tidal_title:
		if tidal_title != previous_title:
			if tidal_title == "TIDAL":
				artist = "Not available"
				song = "Main Menu"
				state = "Not playing anything"
				check += 1
				previous_title = "None"
				if check >= 50:
					check = 0
					presence.update(large_image="logo", large_text="TIDAL Music", details=song, state=artist)
					pprint(state)
					previous_title = tidal_title
			else:
				artist = tidal_title.split(" - ")[1]
				song = tidal_title.split(" - ")[0]
				state = "Currently Listening to " + song + " by " + artist
				pprint(state)
				presence.update(large_image="logo", large_text="TIDAL Music", details=song, state=artist)
				previous_title = tidal_title
	if not tidal_title:
		presence.clear()
	time.sleep(0.05)
