#!/usr/bin/env python

# wallpaper.py
# By Dan Saunders
# Pulls a beautiful wallpaper for each X output, correct resolution and all

# Setting this to true enables terminal debugging output
DEBUG = True

# Choose between 'feh', 'xfce', 'cinnamon', or 'gnome'
DESKTOP = 'xfce'

from os import makedirs
from os.path import dirname, exists, realpath
from random import randint
from re import I, findall
from subprocess import check_output
from time import sleep
from urllib.request import Request, urlopen

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1)'

def get_wallpaper(display, resolution):
	request = Request('http://interfacelift.com/wallpaper/downloads/random/fullscreen/{}/'.format(resolution))
	request.add_header('User-Agent', USER_AGENT)

	if DEBUG: print('Searching "{}" for wallpapers'.format(request.full_url))

	try:
		request = Request('http://interfacelift.com{}'.format([match for match in findall(r'(/wallpaper/[a-z0-9]+/[a-z0-9_]+\.jpg)', urlopen(request).read().decode('utf-8'), I) if not match.startswith('/wallpaper/preview')][0]))
	except
		if DEBUG: print('Could not fetch wallpaper')
		exit()

	request.add_header('User-Agent', USER_AGENT)

	path = '{}/wallpapers/'.format(dirname(realpath(__file__)))
	filename = '{}-{}.jpg'.format(display, randint(0, 10))

	if not exists(path):
		makedirs(path)

	if DEBUG: print('Saving wallpaper "{}" as "{}"'.format(request.full_url, path + filename))

	f = open(path + filename, 'w+b')
	f.write(urlopen(request).read())
	f.close()

	return path + filename

def get_displays():
	displays = check_output('xrandr | grep -e "\\bconnected" | cut -d" " -f1', shell=True).decode('utf-8').strip().split('\n')
	resolutions = check_output('xrandr | grep "\*" | cut -d" " -f4', shell=True).decode('utf-8').strip().split('\n')
	
	return dict(zip(displays, resolutions))

if __name__ == '__main__':
	displays = get_displays().items()
	wallpapers = [get_wallpaper(display, resolution) for (display, resolution) in displays]

	if DESKTOP == 'xfce':
		# TODO: Proper multi-monitor support
		check_output(['xfconf-query', '-c', 'xfce4-desktop', '--property', '/backdrop/screen0/monitor0/image-path', '--set', wallpapers[0]]).decode('utf-8')
	elif DESKTOP == 'cinnamon':
		# TODO: Multi-monitor support
		check_output(['gsettings', 'set', 'org.cinnamon.desktop.background', 'picture-uri', 'file://{}'.format(wallpapers[0])])
	elif DESKTOP == 'feh':
		check_output(['feh', '--bg-scale'] + wallpapers).decode('utf-8')

