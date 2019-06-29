import re
import urls
import twitterpostbot

def userInput():
	
	"""Handles the user interface by using a while-loop that ends when the user enters Q."""
	
	C = False
	q = True
	while q == True:
		i = 0
		cmd = raw_input("What would you like to do?: ")
		cmd = cmd.split()
		if cmd[0] == "C":
			if 4 > len(cmd) > 2:
				infile = cmd[1]
				outfile = cmd[2]
				C = True
				output = open(outfile, 'w+')
				with open(infile,'r') as tweets:
					for line in tweets:
						tweet = Tweet(line)
						if tweet.Haiku():
							i += 1
							output.write(str(i) + " " + tweet.Haiku() + "\n")
				output.close()
				print("Your tweets have been turned into haiku's.")
				print("You can read them with the [R] command or upload specific lines with [U <number>].")
			else:
				print("Please give an input and an output file!")
		elif cmd[0] == "R":
			if C == True:
				output = open(outfile, 'r')
				for line in output:
					print(line)
			else:
				print("You must first compile your file!")
		elif cmd[0] == "U":
			if C == True:
				if len(cmd) > 1:
					if cmd[1].isdigit():
						output = open(outfile, 'r')
						for line in output:
							i += 1
							if str(i) == cmd[1]:
								print(line)
								twitterbot.upload(line[2:])
								print("Uploaded:")
								print(line[2:])
				else:
					print("Please specify the haiku number that you want to upload")
			else:
				print("You must first compile your file!")
		elif cmd[0] == "Q":
			print("Thank you for using the haiku twitter bot, i hope you enjoyed it!")
			q = False
		else:
			print("Invalid command!")
		print("[Q] to quit")

def main():
	
	"""Initiates the program and runs the user interface."""
	
	print("Welcome to the haiku twitter bot, created by Jeroen Boers!")
	print("You have three options:")
	print("[C <inputfile> <outputfile>] to compile your tweets and write them to a file.") 
	print("[R] to read your haiku's.")
	print("[U <number>] to upload a specific line.")
	print("[Q] to quit!")
	print("You must first compile, then read, and then upload a line that you like.")
	q = userInput()
		
				
	

		
class Woord:
	
	"""Creates an object and checks if it is in the worldlist, then if it is found it will give it a few attributes,
	which are a the phonetic pronounciation, list of the phonetic pronounciation split on their syllables,
	the syllable with the accent, and it will make one for the syllable with the accent stripped of the extra character., and lastly the length
	of the list of syllables, mainly for convenience."""
	
	def __init__(self, woord):
		self.woord = woord.lower()
		self.Found = False
		with open('dpw.cd', 'r') as Woordenboek:
			for line in Woordenboek:
				if self.woord in line:
					self.tempLijst = line.split("\\")
					if self.tempLijst[1] == self.woord:
						self.Found = True
						self.Wline = line
						self.woordlijst = self.tempLijst
			if not self.Found:
				self.woordlijst = list(self.woord)
		if self.Found:
			self.fonetisch = self.woordlijst[3]
			self.ktlijst = self.fonetisch.split("-")
			self.klemtoon = [x for x in self.ktlijst if "'" in x]
			self.klemtoonstripped = "".join(re.findall(r"[^\'-]+", self.fonetisch.lower()))
		else:
			self.ktlijst = [1]
			self.klemtoon = [1]
		self.lengte = len(self.ktlijst)

	def printLine(self):
		
		"""Prints the line in the document that contains the word."""
		
		print(self.Wline)

class Tweet:
	
	"""Creates an object that can be tokenized and converted into a haiku."""
	
	def __init__(self, tweet):
		self.tweet = tweet
		
	def tokenize(self):
		
		"""Tokenizes the tweet by removing emoticons, phone numbers, websites, twitter usernames, hashtags and other word types that should not be
		in the haiku."""
		
		emoticon_string = r"""
			(?:
			  [<>]?
			  [:;=8]                     # eyes
			  [\-o\*\']?                 # optional nose
			  [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth      
			  |
			  [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
			  [\-o\*\']?                 # optional nose
			  [:;=8]                     # eyes
			  [<>]?
			)"""
		regex_strings = (
			# Phone numbers:
			r"""
			(?:
			  (?:            # (international)
				\+?[01]
				[\-\s.]*
			  )?            
			  (?:            # (area code)
				[\(]?
				\d{3}
				[\-\s.\)]*
			  )?    
			  \d{3}          # exchange
			  [\-\s.]*   
			  \d{4}          # base
			)"""
			,
			# Emoticons:
			emoticon_string
			,    
			# HTML tags:
			 r"""<[^>]+>"""
			,
			# HTML links:                          # this one is extremely long so i'm importing it
			urls.URL_REGEX
			,
			# Twitter username:
			r"""(?:@[\w_]+)"""
			,
			# Twitter hashtags:
			r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
			,
			# Remaining word types:
			r"""
			(?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
			|
			(?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
			|
			(?:[\w_]+)                     # Words without apostrophes or dashes.
			|
			(?:\.(?:\s*\.){1,})            # Ellipsis dots. 
			|
			(?:\S)                         # Everything else that isn't whitespace.
			"""
			)

		word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
		self.tokens = word_re.findall(self.tweet)
		self.username = self.tokens[0]
		self.tokens.pop(0)	
		self.woorden = [x for x in self.tokens if x.isalpha()]
		self.woorden = [token for token in self.woorden if "amp" not in token and "lt" not in token]
		
	def printLine(self):
		
		"""Prints the tweet after it has been tokenized."""
		
		self.tokenize()
		print(self.woorden)
	
	def doubleletter(self,x,splitletter,soort):
		
		"""This function will take any word that has been split and checks if it contains the same letter around the letter that is has been 
		 split on. If this is true it will return a 1 so the other functions can make sure it is split on the right letter."""
		
		medeklinkers = 'bcdfghjklmnpqrstvwxz'
		try:
			if splitletter == "i" and x[(x.find(splitletter) + 1)] == "e":
				return 1
			elif soort == 2:
					if x[splitletter] == x[splitletter + 1]:
						return 1	
					else:
						return 0
			elif x[x.find(splitletter)] in medeklinkers or x[(x.find(splitletter) + 1)] in medeklinkers:
				if soort == 1 and len(x) > 3:
					if x[x.find(splitletter)] == x[(x.find(splitletter) + 1)]:
						return 1
					else:
						return 0
				else:
					return 0
			else:
				return 0
		except IndexError:
			return 0
				
		
	def splitword1(self,x,y):
		"""Splits a word, only if it has to be split on the first syllable, by looking at the last letter of the first syllable or the first letter
		of the second syllable. If this doesn't work it will split on the length of the length of the last part of the word and it also accounts for
		double letters when it splits."""
		if y.ktlijst[1][0].lower() in x:
			splitletter = y.ktlijst[1][0].lower()
		elif y.ktlijst[1][1].lower() in x:
			splitletter = y.ktlijst[1][1].lower()
		else:
			deel1 = x[:y.fonetisch.find("-")]
			deel2 = ''.join(x.split(deel1, 1))
			return deel1,deel2
		if x[0] == splitletter:
			pos = -1
			for q in xrange(2):
				pos = x.find(splitletter, pos+1)
			indexletter = pos
			deel1 = x[:(indexletter + self.doubleletter(x,indexletter,2))]	
		else:
			deel1 = x[:(x.find(splitletter) + self.doubleletter(x,splitletter,1))]
		deel2 = ''.join(x.split(deel1, 1))
		return deel1,deel2
		
	def splitword2(self,x,y):
		
		"""Does the same as splitword1, except for if a word has to be split on the second syllable. Because of the possibility of a letter
		being in multiple places in a word it also looks for doubles and checks which one it has to be split on."""
		
		if y.ktlijst[2][0].lower() in x[1:]:
			q=1
			splitletter = y.ktlijst[2][0].lower()
		elif y.ktlijst[2][1].lower() in x[1:]:
			q=2
			splitletter = y.ktlijst[2][1].lower()
		else:
			deel1 = x[:-(len(y.ktlijst[-1]))]
			deel2 = ''.join(x.split(deel1, 1))
			return deel1,deel2
		if x.count(splitletter) == 1:
			if q == 1:
				deel1 = x[:(x.find(splitletter) + self.doubleletter(x,splitletter,1))]
			if q == 2:
				deel1 = x[:(x.find(splitletter) + self.doubleletter(x,splitletter,1))]				
		elif x.count(splitletter) > 1:
			pos = -1
			for g in xrange(2):
				pos = x.find(splitletter, pos+1)
			indexletter = pos
			deel1 = x[:(indexletter + self.doubleletter(x,indexletter,2))]			
		deel2 = ''.join(x.split(deel1, 1))
		return deel1,deel2
		
	def Haiku(self):
		
		"""Takes a tweet and turns it into a haiku.
		
		It will check how many words are in the tweet and if it contains 17 it will give a haiku as output. 
		If a word is more than 1 syllable and the tweet has 4  or 11 syllables up until that word, it will split it on the first syllable of the word,
		if it has more than 2 syllables and the tweet has 3 or 10 words up until that word it will split the word on the second part of the word."""
		
		self.tokenize()
		haiku1 = []
		haiku2 = []
		haiku3 = []
		totaalLG = 0
		for x in self.woorden:
			x = x.lower()
			y = Woord(x)
			woordLG = int(y.lengte)
			if (totaalLG) in (4,11) and woordLG > 1:
				deel1,deel2 = self.splitword1(x,y)
				if totaalLG == 4:
					haiku1.append(deel1 + "-")
					haiku2.append(deel2)
				else:
					haiku2.append(deel1 + "-")
					haiku3.append(deel2)
			elif totaalLG in (3,10) and woordLG > 2:
				deel1,deel2 = self.splitword2(x,y)
				if totaalLG == 3:
					haiku1.append(deel1 + "-")
					haiku2.append(deel2)
				else:
					haiku2.append(deel1 + "-")
					haiku3.append(deel2)
			else:
				if (totaalLG + woordLG) < 6:
					haiku1.append(x)
				elif 5 < (totaalLG + woordLG) < 13 and totaalLG > 4:
					haiku2.append(x)
				elif (totaalLG + woordLG) > 12 and totaalLG > 11:
					haiku3.append(x)
			totaalLG = totaalLG + woordLG
		if totaalLG == 17 and haiku1 and haiku2 and haiku3:
			self.haiku = ' '.join(haiku1) + ', ' + ' '.join(haiku2) + ', ' + ' '.join(haiku3) + '.'
			self.haiku = self.haiku.capitalize()
			return self.haiku
		
main()
