#import modules used
from time import sleep
import shelve
import os

def displayOptions(*args,back=True,clear=""):
	'''shows options to the user for any given arguments and includes '<--back' unless specified, includes clear if specified'''
	
	#clear, if selected clears the terminal/powershell screen
	if clear:
		os.system('cls' if os.name == 'nt' else 'clear')
	print("\nSelect an option\n")
	#for all the arguments given, display them in order
	for arg in args:
		tempArg = arg
		#check if argument is function, if so, use doc string as text to display (may not be best practice)
		if callable(arg):
			tempArg = arg.__doc__
		print(str(args.index(arg)+1)+".-- "+tempArg+"\n")
	lenListInt = len(args)+1
	#back, includes option at the bottom of the list to return to main function
	if back:
		print(str(len(args)+1)+".-- <--Back \n")
		lenListInt+=1
	#loop to ensure input given is correct
	while True:
		try:
			selectedOption = int(input("Please select one: "))
			if selectedOption not in range(1,lenListInt):
				raise ValueError
			else:
				break
		except ValueError:
			print('\n *** please enter a valid number *** \n')
	print("\n **** \n \n")
	return selectedOption-1 #-1 to make it easier indexing lists

def formatScores(scoreList):
	'''Format the scores given from list of tuples'''
	
	#Headings for table
	scoreString = 'Scores'
	userString = 'Username'
	dateString = 'Datetime'
	wordSetString = 'Word Set'
	#format for each row
	stringFormat = '|{:^10}|{:^15}|{:^28}|{:^15}|'
	print(stringFormat.format(scoreString,userString,dateString,wordSetString))
	#inbetween line (magic number not ideal)
	print('-'*73)
	#print each tuple (score)
	for i in scoreList:
		print(stringFormat.format(i[0],i[1],i[2],i[3]))
		sleep(0.1)
	sleep(1)

def shelveWriteCreate(myKey,myValues):
	'''Writes to shelve file using key and value given, creates if not available'''
	with shelve.open('data-file','c') as shelf:
		shelf[myKey] = myValues

def shelveRead(myKey):
	'''Reads from the shelve file at the key location and returns the values'''
	with shelve.open('data-file','r') as shelf:
		return shelf[myKey]

