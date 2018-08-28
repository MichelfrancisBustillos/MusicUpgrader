import requests
import json
import csv
import sys
import os
import configparser
import yaml
import atexit
import ID3

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
	fileList = getListOfFiles(musicLibraryPath)
	
	return
	
def cleanup():
	if os.path.exists('tmp'): os.remove('tmp')
	if os.path.exists('downloadLinks.txt'): os.remove('downloadLinks.txt')
	if os.path.exists('trackList.csv'): os.remove('trackList.csv')
	if os.path.exists('SMLoadr.log'): os.remove('SMLoadr.log')
	if os.path.exists('SMLoadrConfig.json'): os.remove('SMLoadrConfig.json')
	return
	
def getListOfFiles(dirName):
	listOfFile = os.listdir(dirName)
	allFiles = list()
	for entry in listOfFile:
		fullPath = os.path.join(dirName, entry)
		if os.path.isdir(fullPath):
			allFiles = allFiles + getListOfFiles(fullPath)
		else:
			allFiles.append(fullPath)

	count = 0
	for i in allFiles:
		format = i
		format = format[format.rfind('.'):]
		name = i
		a = name.rfind('\\')
		b = name.rfind('.')
		name = name[a:b]
		if not format in open('fileFormats.txt').read():
			print("Name: " + name + " Format: " + format)
			del allFiles[count]
		count = count + 1
	
	return allFiles
	
def createLinkList(trackListPath, errorListPath, downloadListPath):
	with open(trackListPath, 'r') as csvfile, open(errorListPath, 'w') as errorList, open(downloadListPath, 'w') as linkList:
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
trackListPath = config['DEFAULT']['Track List Path']

if not os.path.exists(trackListPath):
	print("Error! Track List not found!\n")
	print("1) I have one.\n")
	print("2) I would like to create one.\n")
	trackListChoice = input("> ")
	if trackListChoice == '1':
		trackListPath = input("Enter track list path: ")
		if os.path.exists('configuration.config'):
			config['DEFAULT']['Track List Path'] = trackListPath
			config.write(open('configuration.config', 'w'))
		else:
			print("Error! Track list non-existant!")
	elif trackListChoice == '2':
		print("Sorry! This option is not yet available.\n")
		print("You can create one manually by installing beets and running this command: \n")
		print("beet ls -f \"$artist, $title\" > trackList.csv\n")
		input("Press enter to exit.")
		createTrackList()
		
	createLinkList(trackListPath, errorListPath, downloadListPath)

os.system(".\SMLoadr-win-x86 --quality \"FLAC\" --downloadmode \"all\"")

