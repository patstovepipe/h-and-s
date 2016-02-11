# parser.py

import string

# 'trip' represents a single street and it's house numbers.

suffix_comma = ['st,', 'street,','rd,', 'road,', 'dr,', 'drive,', 'ave,', 'avenue,', 'pl,', 'place,', 'tce,', 'lane,', 'ln,', 'park,', 'prk,',]
suffix = ['st', 'street','rd', 'road', 'dr', 'drive', 'ave', 'avenue', 'pl', 'place', 'tce', 'lane', 'ln', 'park', 'prk',]

delimiters = [',', '/']

oddcode = ['odd', '#odd', 'odd#', 'odd,', '#odd,', 'odd#,']
evencode = ['even#', '#even', 'even', 'even,', '#even,', 'even#,',]

# parsetrips()
#
# 1. Determine the location of the suffixes rd, ave, etc for each trip
# 2. Determine when the next comma or forward slash (delimiter) occurs
# 3. Using the next delimiter occurence, seperate the words into 
#    seperate lists for each trip.
# 
#	 Commas often seperate individual house numbers from ranges of house
#	 numbers, so using them exclusively as trip delimiters won't work.
#	 An example would be '...101-141, 151 River St, ...' 
#	 Instead, we find the occurence of a suffix, which occurs once per
# 	 trip, and look ahead for the next delimiter. Everything behind the
#	 next delimiter is put in an unordered list, which is handled later.

def parsetrips(str):
	str = str.lower()
	words = str.split()
	output = [] 			# output is a list of unordered lists of 
	endoftrip = 0			# trip details for each trip in route desc.
	print 'length of words: ', len(words), '\nThe initial list:\n', words, '\n\n'
	while len(words) >= 1:
		for word in words:
			print 'examining word: ' + word
			if word in suffix_comma:
				endoftrip = words.index(word) + 1
				break
			elif word in suffix:
				print '\nword ', word, ' is in suffix. Looking for next delimiter:'
				for i in range(words.index(word), len(words)):
					print 'is the next delimiter ', words[i], '?',
					if words[i][-1] in delimiters:
						print 'yes!'
						endoftrip = i + 1
						break
				break
		output.append(words[:endoftrip])
		words = words[endoftrip:]
		print 'iteration complete. remaining words:\n', words, '\nnew output:\n', output, '\n\n' 
	return output
