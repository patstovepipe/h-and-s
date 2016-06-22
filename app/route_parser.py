# parser.py

from export import Export
import sys
from openpyxl import load_workbook
import getopt
import string
import time

# 'trip' represents a single street and it's house numbers.
suffix_comma = ['st,', 'street,','rd,', 'road,', 'dr,', 'drive,', 'ave,', 'avenue,', 'pl,', 'place,', 'tce,', 'lane,', 'ln,', 'park,', 'prk,',]
suffix = ['st', 'street','rd', 'road', 'dr', 'drive', 'ave', 'avenue', 'pl', 'place', 'tce', 'lane', 'ln', 'park', 'prk',]

delimiters = [',', '/']
oddcode = ['odd', '#odd', 'odd#', 'odd,', '#odd,', 'odd#,']
evencode = ['even#', '#even', 'even', 'even,', '#even,', 'even#,',]

# Importing filename from command line, and collecting the data
def init():

    args = sys.argv[1:]
    if len(args) == 0:
        route = raw_input("> [route_parser] Insert a route to query with, or nothing to run a test route.] \n \
                           > ")
        if len(args) == 0:
            route = "4-40 Beach Dr Even#, 650-776 Mountjoy Ave Even#, 2019-2027 Runnymede Ave Odd# (19)"
            print "[route_parser] No args provided - Running the following test route: "
            print route
        parsedroute = parse(route)
        print "[route_parser] Parsed the test route: \n", parsedroute
        ex = Export()
        ex.set_login_details("","")
        for each in parsedroute:
            if each == []:
                continue
            parsed_routes = {"Street": each[0]}
            ex.set_search_dict(parsed_routes)
            ex.generate_excel()
            time.sleep(5)
        print "[route_parser] Successfully parsed route description and wrote data to file."
        return

    wb = load_workbook(filename = '%s' % args[0], read_only=True)
    ws = wb[wb.get_sheet_names()[0]]
    print ws
    result = []
    for row in ws.iter_rows():
        for cell in row:
            if cell.column == 5 and cell.value != None:
                print cell.value

    print result

# parse_trips()
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
#
# Suppose we input this route into the above parser:
# 4-40 Beach Dr Even#, 650-776 Mountjoy Ave Even#, 2019-2027 Runnymede Ave Odd# (19)
# The output will look like this:
# [['4-40', 'beach', 'dr', 'even#,'], ['650-776', 'mountjoy', 'ave', 'even#,'], ['2019-2027', 'runnymede', 'ave', 'odd#'], ['(19)']]
def parse_trips(str):
	str = str.lower()
	words = str.split()
	output = []
	endoftrip = 0
	while len(words) >= 1:
		for word in words:
			if word in suffix_comma:
				endoftrip = words.index(word) + 1
				break
			elif word in suffix:
				for i in range(words.index(word), len(words)):
					if words[i][-1] in delimiters:
						endoftrip = i + 1
						break
				break
		output.append(words[:endoftrip])
		words = words[endoftrip:]
	return output

# organize_trip()
#
#    Takes one list of assorted details, including street name, suffix, house
#	 numbers and a string that specifies odd or even for those numbers.
#    See the comments for parse_trips.
#
# 1. Create a new list and make the first item a string of the street name.
# 2. Generate a list of ints that match the conditions in the list of details,
#    and make that list the second item of the new list.
# 3. Return the new list.
def organize_trip(lst):
	if len(lst) <= 1:
		return []
	streetnameposlist = []
	housenumberlist = []
	housenumbers = []
	for word in lst:
		if word in suffix:
			streetnameposlist.append(lst.index(word)-1)
			streetnameposlist.append(lst.index(word))
		if word[0] in string.digits:
			housenumberlist.append(word)
	streetname = lst[streetnameposlist[0]] + " " + lst[streetnameposlist[1]]
	for word in housenumberlist:
		if '-' in word:
			boundarylist = word.split('-')
			for i in range(int(boundarylist[0]), int(boundarylist[1]), 2):
				housenumbers.append(i)
		else:
			housenumbers.append(int(word))
	output = [streetname, housenumbers]
	return output

def parse(route):
	parsed_items = []
	trips = parse_trips(route)
	for each in trips:
		parsed_items.append(organize_trip(each))
	return parsed_items

if __name__=="__main__":
    init()
