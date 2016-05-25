import sys
import os

import xlsxwriter

"""

Test Data

"""

routelist1 = ['Data-set-1', 'Jim street', 2000, 2001, 2002, 2005, 'Bob Avenue', 1300, 1400, 1500]

routelist2 = ['Data-set-2', 'Pavi Place', 1000]

routelist3 = ['Data-set-3', 'Jim Street', 100, 100, 'Bob Place', 'Bob Place']

testdata =[routelist1, routelist2, routelist3]


if len(sys.argv) == 1:
	print("No arguement provided, please provide test data set.")
	sys.exit()

if len(sys.argv) > 2:
	print("Error, too many arguements provided.")
	sys.exit()

testroute = sys.argv[1]

for route in testdata:
	if testroute in route:
		print("Testing with: " + testroute)
		if testroute == "Data-set-1":
			testroute = routelist1
		if testroute == "Data-set-2":
			testroute = routelist2
		if testroute == "Data-set-3":
			testroute = routelist3

		break

testroute = testroute[1:]
print(testroute)

"""

Start making spreadsheet here.


"""

workbook = xlsxwriter.Workbook('testroute.xlsx')
worksheet = workbook.add_worksheet()

x = 0
y = 0

worksheet.write(0, 0, "Road Name")
worksheet.write(0, 1,  "House #'s")

for item in testroute:
	if type(item) is str:
		y += 1
		x = 0
		worksheet.write(y, x, item)
	elif type(item) is int:
		x += 1
		worksheet.write(y, x, item)

workbook.close()
print("Done Writing")
















