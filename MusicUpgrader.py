import requests
import json
import csv
import sys
import os
import configparser
import yaml
import atexit

def getTrackLink(artist, track):
	url = "https://api.deezer.com/search"

	querystring = {"q":"artist:\"" + artist + "\" track:\"" + track + "\""}

	response = requests.request("GET", url, params=querystring)

	response = response.json()
	
	try:
		link = response["data"][0]["link"]
	except IndexError:
		link = "Error!"
		
	return link
	
def createTrackList():
	musicLibraryPath = input("Enter the path to your music library: ")
	config['DEFAULT']['Music Library Path'] = musicLibraryPath
	config.write(open('configuration.config', 'w'))
	os.system("pip install beets")
	os.system('beet config -p > tmp')
	beetConfigPath = open('tmp', 'r').read().rstrip()
	with open(beetConfigPath, 'w') as beetConfig:
		beetConfigData = str("directory: " + musicLibraryPath + "\nlibrary: " + musicLibraryPath + "\musiclibrary.db\n")
		print(beetConfigData)
		yaml.dump(beetConfigData, beetConfig, default_flow_style = False)
	beetConfig.close()
	os.system(str("beet import -a " + musicLibraryPath))
	os.system('beet ls -f \"$artist, $title\" > trackList.csv')
	return
	
def cleanup():
	if os.path.exists('tmp'): os.remove('tmp')
	if os.path.exists('downloadLinks.txt'): os.remove('downloadLinks.txt')
	if os.path.exists('trackList.csv'): os.remove('trackList.csv')
	if os.path.exists('SMLoadr.log'): os.remove('SMLoadr.log')
	if os.path.exists('SMLoadrConfig.json'): os.remove('SMLoadrConfig.json')
	return


atexit.register(cleanup)
config = configparser.ConfigParser()
if os.path.exists('configuration.config'):
	print("Config file found!")
	config.read('configuration.config')
else:
	print("No config file found! Generating one...")
	config['DEFAULT'] = {'Track List Path' : 'trackList.csv',
	                     'Download Link List Path' : 'downloadLinks.txt',
						 'Error List Path' : 'errorList.txt',
						 'Music Library Path' : 'C:\\Users\\%%username%%\\Music'}
	config.write(open('configuration.config', 'w'))
						 
errorListPath = config['DEFAULT']['Error List Path']
downloadListPath = config['DEFAULT']['Download Link List Path']

filePath = config['DEFAULT']['Track List Path']

if not os.path.exists(filePath):
	print("Error! Track List not found!\n")
	print("1) I have one.\n")
	print("2) I would like to create one.\n")
	trackListChoice = input("> ")
	if trackListChoice == '1':
		filePath = input("Enter track list path: ")
		config['DEFAULT']['Track List Path'] = filePath
		config.write(open('configuration.config', 'w'))
	elif trackListChoice == '2':
		print("Sorry! This option is not yet available.\n")
		print("You can create one manually by installing beets and running this command: \n")
		print("beet ls -f \"$artist, $title\" > trackList.csv\n")
		input("Press enter to exit.")
#		createTrackList()

with open(filePath, 'r') as csvfile, open(errorListPath, 'w') as errorList, open(downloadListPath, 'w') as linkList:
	listFile = csv.reader(csvfile, delimiter=',', quotechar="|")
	for row in listFile:
		artist = row[0]
		track = row[1]
		print ("Artist: ", artist, " Track: ", track)
		link = getTrackLink(artist, track)
		if link == "Error!":
				errorList.write(str("Artist: " + artist + " Track: " + track + "\n"))
		else:
				linkList.write(str(link + "\n"))

csvfile.close()
errorList.close()
linkList.close()

os.system(".\SMLoadr-win-x86 --quality \"FLAC\" --downloadmode \"all\"")

