#!/usr/bin/env python

# wallpaper.py
# By Dan Saunders
# Pulls a beautiful wallpaper for each X output, correct resolution and all

from glob import glob
from os import makedirs
from os.path import dirname, exists, realpath
from random import randint
from re import I, findall, sub
from subprocess import check_output
from time import sleep
from urllib.request import Request, urlopen

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'

def get_wallpaper(display, resolution):
	request = Request('http://interfacelift.com/wallpaper/downloads/random/fullscreen/{}/'.format(resolution))
	request.add_header('User-Agent', USER_AGENT)

	try:
		request = Request('http://interfacelift.com{}'.format([match for match in findall(r'(/wallpaper/[a-z0-9]+/[a-z0-9_]+\.jpg)', urlopen(request).read().decode('utf-8'), I) if not match.startswith('/wallpaper/preview')][0]))
	except:
		exit()

	request.add_header('User-Agent', USER_AGENT)

	path = '{}/wallpapers/'.format(dirname(realpath(__file__)))
	filename = '{}-{}.jpg'.format(display, randint(0, 10))

	if not exists(path):
		makedirs(path)

	f = open(path + filename, 'w+b')
	f.write(urlopen(request).read())
	f.close()

	return path + filename

def get_displays():
	displays = {}
	files = glob('/sys/class/drm/card*/modes')
	devices = [sub(r'^.*card[0-9]-([a-z]+)(-I)?-([0-9]+)/modes$', r'\1\3', device_file, flags=I) for device_file in files]
	
	for index in range(len(files)):
		resolutions = open(files[index], 'r').read().strip()
		
		if resolutions:
			displays[devices[index]] = resolutions.split()[0]
	
	return displays

if __name__ == '__main__':
	# Uncomment if you use XFCE
	# TODO: Proper multi-monitor support
	check_output(['xfconf-query', '-c', 'xfce4-desktop', '--property', '/backdrop/screen0/monitor0/image-path', '--set', [get_wallpaper(display, resolution) for (display, resolution) in get_displays().items()][0]]).decode('utf-8')

	# Uncomment if you use Cinnamon
	# TODO: Multi-monitor support
	#check_output(['gsettings', 'set', 'org.cinnamon.desktop.background', 'picture-uri', 'file://{}'.format([get_wallpaper(display, resolution) for (display, resolution) in get_displays().items()][0])])

	# Uncomment if you use feh (used in smaller window managers)
	#check_output(['feh', '--bg-scale'] + [get_wallpaper(display, resolution) for (display, resolution) in get_displays().items()]).decode('utf-8')

