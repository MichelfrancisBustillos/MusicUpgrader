# MusicUpgrader

A script/program that takes a CSV file with song artists and names and downloads each song at the highest quality available (FLAC preferred) via a free Deezer account and SMLoadr.

You can generate the CSV file manually using Microsoft Excel or any other spreadsheet program. Simply list the artist in column A and song title in column B, then save the list as a CSV (Comma Seperated Value) file. I will eventually upload a sample CSV file which you can use to test the program.
Alternatively, you can generate a list of your current music library using beets. Install beets with `pip install beets`. Then import your library to it with `beet -A /path/to/your/library/`. Finally, ouput the CSV file with `beet ls -f "$artist, $title" > output.csv`.

Function List (For my sanity):
	`createLinkList`: Takes CSV file of Songs with Title and Artist and outputs txt file of links for SMLoadr to download
	`getListOfFiles`: Takes library directory and outputs a list() of all files of types defined in fileFormats.txt
	`createTrackList`: Takes list() of files, parses metadata, and outputs csv file with songs Title and Artist
	`cleanup`: Closes and deletes files when program closes
