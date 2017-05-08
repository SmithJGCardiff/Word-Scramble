#Importing modules
import os
from time import sleep, ctime
import shelve
import random
#Modules I have created stored in wordScrambleModules
from wordScrambleModules import formatScores, displayOptions, shelveWriteCreate, shelveRead

#Defining the functions before being called in the game loop
def gameLoop():
	'''Keep the game running'''
	while True:
		#check if there are any sources, user cannot proceed without words loaded
		availableSources = getAvailableSources()
		#clear screen for formatting
		os.system('cls' if os.name == 'nt' else 'clear')
		welcomeMessage = "\n ****\nWelcome to Word Jumble\nUnscramble the letters to make a word."
		print(welcomeMessage)
		sleep(1)
		#choose what to do
		optionChosen = displayOptions(playGame,browseSets,addSet,deleteSet,sortedScores,exitGame,back=False)
		if optionChosen == 0:
			playGame()
		elif optionChosen == 1:
			browseSets()
		elif optionChosen == 2:
			addSet()
		elif optionChosen == 3:
			deleteSet()
		elif optionChosen == 4:
			sortedScores()
		elif optionChosen == 5:
			exitGame()

def getAvailableSources():
	'''Function to populate a list with the different word sets available'''
	availableSources = []
	#Loop to ensure that word sets are found, if none are available, they must be added from file
	while True:
		try:
			#check shelf file for word sets, if there are none or there are just scores, raise exception
			with shelve.open('data-file','r') as shelf:
				if (bool(shelf.keys()) == False) or (list(shelf.keys())== ['scores']) :
					raise
				else:
					#add all the keys that aren't already in available sources and that aren't scores to the list
					for key in shelf.keys():
						if (repr(key) not in availableSources) and (key != 'scores') :
							availableSources.append(key)
		except:
			#this error will appear if there are no words shelved in the file, 
			#user must have words to play, so user has option to add words
			print("Before you can play the game you need to have some words \nPlease add some now, view your scores, or come back later")
			optionChosen = displayOptions(addSet,sortedScores,exitGame,back=False)
			if optionChosen == 0:
				addSet()
			elif optionChosen == 1:
				sortedScores()
			elif optionChosen == 2:
				exitGame()
		else:
			#break the loop if the try clause has no problems
			break
	return availableSources

def playGame():
	'''Play the game'''
	#refresh available sources
	availableSources = getAvailableSources()
	#choose word set to play with
	optionChosen = displayOptions(clear=True,back=False,*availableSources)
	#user has chosen <-- back
	if optionChosen == len(availableSources):
		return
	#index available sets with user choice
	groupChosen = availableSources[optionChosen]
	#return list of words from shelf file
	wordList = shelveRead(groupChosen)
	#choose a sample of 10 numbers from 1 to the amount of words available and index those words from the wordList
	randWordSample = [wordList[i] for i in random.sample(range(len(wordList)), 10)]
	#user starts with score of 0
	correctScore = 0

	for word in randWordSample:
		#loop to ensure that when the word is shuffled, the same word is not returned
		shuffledWord = word
		while word == shuffledWord:
			shuffledWord = ''.join(random.sample(list(word),len(word)))
		#print the word for the user
		print('\n',randWordSample.index(word)+1,'.-- ',shuffledWord,'\n',sep='')
		# userGuess = input('Your guess: ').lower()
		userGuess = "sad"
		#sanitise user guess just in case they included a space they couldn't see
		if userGuess.strip() == word:
			print('correct')
			correctScore += 1
		else:
			print('incorrect, the word is',word)
		sleep(0.6)

	#End of quiz responses based on scores, any number of these can be included
	if correctScore > 4:
		print('Congratulations, you scored {} out of 10'.format(correctScore))
	else:
		print('Unlucky, you only scored {} out of 10'.format(correctScore))
	sleep(3)
	#username for the scoreboard
	print('\n****\nPlease enter a 3 letter nickname for the leaderboard\n****\n')
	userName = ""
	while len(userName) != 3:
		userName = input('---:')
	#create tuple of all relevant information
	scoreTup = (correctScore,userName,ctime(),groupChosen)
	#try to write to shelf file if it exists
	try:
		with shelve.open('data-file','w') as shelf:
			scoreList = shelf["scores"]
			scoreList.append(scoreTup)
			shelf["scores"] = scoreList
	#if there is no shelf file, create one
	except:
		scoreList = []
		scoreList.append(scoreTup)
		with shelve.open('data-file','w') as shelf:
			shelf["scores"] = scoreList

def browseSets():
	'''Browse a word set'''
	#refresh available sources in case user has recently added one
	availableSources = getAvailableSources()
	#user chooses word set to view
	optionChosen = displayOptions(clear=True,*availableSources)
	#user has chosen <--back
	if optionChosen == len(availableSources):
		return
	groupChosen = availableSources[optionChosen]
	#retrieve word list from shelf file
	with shelve.open('data-file','r') as shelf:
		wordList = shelf[groupChosen]
	#clear screen to make it look nice
	os.system('cls' if os.name == 'nt' else 'clear')
	#print title of the group
	print("*"*(len(groupChosen)+4)+'\n* '+groupChosen+' *\n'+'*'*(len(groupChosen)+4))
	sleep(0.6)
	#print each word on new line, use sleep(0.2) to create effect 
	for i in wordList:
		print("*",i.capitalize(),"*",end="\n")
		sleep(0.2)
	print("*"*20)
	#user can return to main menu
	optionChosen = displayOptions()
	if optionChosen==0:
		return

def addSet():
	'''Add a new word set from current directory'''
	##Function to add new set of words to the game, with setName as the name of the set

	#find all the files in the current directory (using os module for compatibility between OSX and Windows)
	files = filter(os.path.isfile, os.listdir(os.curdir))
	#return a list of all the text files from the list of files
	files = [f for f in os.listdir(os.curdir) if f.endswith('.txt')]
	#if there are no text files, inform the user to add a text file and try again
	if files == []:
		print("I'm sorry, you need to add text files to the current directory in order to add them to the game\n")
		exitBool = displayOptions(exitGame,back=False,)
		if exitBool == 0:
			exitGame()
	#show user list of text files
	optionChosen = displayOptions(clear=True,*files)
	#user has selected <--back
	if optionChosen == len(files):
		return
	#user has selected exit
	elif optionChosen == len(files)+1:
		exitGame()
	#index list of files with user choice
	setFileName = files[optionChosen]
	#prompt user for set name
	setName = str(input("Name for the new set: "))
	#open text file chosen
	with open(setFileName,'r') as fopen:
		#sanitise the text, and create a list of words
		wordList = [word for line in fopen for word in line.rstrip(',\n').split(', ') if word != '']
	#Ensure that there are the minimum of 10 words needed to play the game
	if len(wordList) >= 10:
		#write to shelf file
		shelveWriteCreate(setName,wordList)
		print('Word set added')
		sleep(2)
	else:
		print("I'm sorry, you need a file with more than ten words, choose a different file and try again")
		return

def deleteSet():
	'''Delete a word set'''
	#refresh words available in case new one has been added
	availableSources = getAvailableSources()
	#choose word set to delete
	optionChosen = displayOptions(clear=True,*availableSources)
	#user has chosen <--back
	if optionChosen == len(availableSources):
		return
	groupChosen = availableSources[optionChosen]
	#open shelf file and delete the word set chosen
	with shelve.open('data-file','w') as shelf:
		del shelf[groupChosen]

	print("*"*20)
	print('Set deleted')
	sleep(2)

def sortedScores():
	'''My sorted scores'''
	while True:
		optionChosen = displayOptions('View scores', 'Delete scores',clear=True)
		#View Scores
		if optionChosen == 0:
			#try to read scores from shelf file if there are any
			try:
				#create list of scores
				scoreList = shelveRead('scores')
				tempScoreList = scoreList[:]
				#print scores in defaut view, i.e score-descending
				#create new list rather than sort in place for simplicity
				descendedScores = []
				#sort scores
				while tempScoreList:
					highestScore = tempScoreList[0]
					for i in tempScoreList:
						if i[0] > highestScore[0]:
							highestScore = i
					descendedScores.append(highestScore)
					tempScoreList.remove(highestScore)
				formatScores(descendedScores)

				#user can view scores ranked by date or score
				dateOrScore = displayOptions('Rank by Date','Rank by Score',back=True)
				if dateOrScore == 0:
					#scores are appended to list so most recent means reverse list, otherwise just print the scores
					ascendOrDescend = displayOptions('Most recent first','Oldest first',back=False,)
					if ascendOrDescend == 0:
						formatScores(scoreList[::-1])
					else:
						formatScores(scoreList)
				elif dateOrScore == 1:
					ascendOrDescend = displayOptions('Highest score first','Lowest score first',back=False)
					if ascendOrDescend == 0:
						formatScores(descendedScores)
					else:
						ascendedScores = []
						while scoreList:
							lowestScore = scoreList[0]
							for i in scoreList:
								if i[0] < lowestScore[0]:
									lowestScore = i
							ascendedScores.append(lowestScore)
							scoreList.remove(lowestScore)
						formatScores(ascendedScores)
				else:
					return
				#once they've finished viewing scores they can return
				optionChosen = displayOptions()
				if optionChosen==0:
					return
			#raise exception if there are no scores
			except:
				print("\n** You haven't played the game yet! **\n\n** Play the game to see your scores **\n")
				sleep(3)
		#user has chosen to delete the scores
		elif optionChosen == 1:
			while True:
				#confirm delete
				boolYesNo = input('Are you sure? (y/n): ')
				if boolYesNo == 'y':
					#try to delete the scores if there are any
					try:
						with shelve.open('data-file','w') as shelf:
							del shelf['scores']
						print(' ****\nScores deleted\n ****')
						sleep(3)
					#tell the user there are no scores
					except:
						print(" ****\nYou haven't got any scores to delete\n ****")
						sleep(3)
					return
				#user has reconsidered 
				elif boolYesNo == 'n':
					return
		#user has chosen <--back
		else:
			return

def exitGame():
	'''Exit'''
	##Function to quit the game
	print("Thanks for playing, goodbye \n")
	quit()


#start the game
gameLoop()
