#!/bin/python3
from presence import Presence
import time
import os

# change dir to where the script is
DIR = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(DIR)

client_id = '451491740499705857' # My ID, please no abuse :(
RPC = Presence(client_id)
RPC.connect() # Magic PyPresence stuff, no idea :(

line1 = os.popen('bash ./gimp-rpc.sh line1').read() # status
line2 = os.popen('bash ./gimp-rpc.sh line2').read() # filename
version = os.popen('bash ./gimp-rpc.sh version').read()

line2old = line2

initresult = os.popen('bash ./init-script.sh').read() # Initialize the script
if initresult.find("ERROR_WMCTRL_NOT_INSTALLED") != -1: 
	date = os.popen('echo -n $(date +%s)').read()
	print(date + ' - wmctrl is not installed. Refer to README.md for more information.')
	exit()
elif initresult.find("ERROR_SCRIPT_ALREADY_RUNNING") != -1: 
	date = os.popen('echo -n $(date +%s)').read()
	print(date + ' - The script is already running! Stopping.')
	exit()


def initcheck():
	initresult = os.popen('bash ./init-script.sh').read() # Initialize the script
	while not (initresult is ''):
		try:
			time.sleep(3)
			initresult = os.popen('bash ./init-script.sh').read() # Initialize the script
			if initresult.find("ERROR_GIMP_NOT_FOUND") != -1: 
				date = os.popen('echo -n $(date +%s)').read()
				print(date + ' - GIMP is not detected. It might be closed.')
			elif initresult.find("ERROR_DISCORD_NOT_FOUND") != -1: 
				date = os.popen('echo -n $(date +%s)').read()
				print(date + ' - Discord is not detected. Please install and/or run the Discord client.')
			elif initresult.find("ERROR_NO_CONNECTION") != -1: 
				date = os.popen('echo -n $(date +%s)').read()
				print(date + ' - There is no Internet Connection to the Discord server!')
			else:
				pass
		except:
			break
		else:
			RPC.clear()
			pass

# details = line1, state = line2

while True:
	initcheck()
	if line2old == line2:
		line2 = os.popen('bash ./gimp-rpc.sh line2').read()
		time.sleep(1)
	else:
		line1 = os.popen('bash ./gimp-rpc.sh line1').read() # status
		line2 = os.popen('bash ./gimp-rpc.sh line2').read() # filename
		version = os.popen('bash ./gimp-rpc.sh version').read()
		time.sleep(1)
		print(RPC.update(details=line1, state=line2, large_image="gimp-papirus", large_text=version))
		if (line2 == 'ERROR_BREAK'):
			RPC.clear()
		line2old = line2

