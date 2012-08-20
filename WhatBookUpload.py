import requests
import sys
from termcolor import colored

# WhatBookUpload - eBook uploader for What.cd.
# https://github.com/dewey/WhatBookUpload

###################################
# CONFIG                          #
###################################

username = ''
password = ''

###################################

payload = {'username':username, 'password':password,'login':'Login', 'keeplogged':'1'}
heads = {'Content-type':'application/x-www-form-urlencoded'}

s = requests.session()
login = s.post('https://ssl.what.cd//login.php', data = payload)
userIndex = s.get('https://ssl.what.cd/ajax.php?action=index')

while True:
	torrent = raw_input(colored('Path to Torrentfile: (enter button to exit)\n', 'yellow'))
	if torrent == "":
		break
	title = raw_input(colored('Title:\n', 'yellow'))
	tags = raw_input(colored('Tags:\n', 'yellow'))
	image = raw_input(colored('Image URL: (optional)\n', 'yellow'))
	desc = raw_input(colored('Description:\n', 'yellow'))

	# Send values via Post
	heads = {'Content-type':'application/x-www-form-urlencoded'}
	s.get('https://ssl.what.cd/upload.php')

	# Build Post Request
	files = {'file_input': (torrent, open(torrent, 'rb'))}
	formData = {'submit':'true', 'type': '2', 'title': title, 'tags': tags, 'image': image, 'desc': desc, 'auth': userIndex.json["response"]["authkey"]}
	r = s.post("https://ssl.what.cd/upload.php", data=formData, files=files)

	print(colored('Status:\n', 'yellow'))
	if "torrents.php" in r.url:
		print(colored('Torrent uploaded successfully! - ' + r.url, 'green'))
	else:
		print(colored('Error - Torrent not uploaded!', 'red'))

	print "\n=============================================="
	print "                NEXT UPLOAD                   "
	print "==============================================\n"

s.get('https://ssl.what.cd/logout.php?auth=' + userIndex.json["response"]["authkey"])
