import os
import sys
import requests
from lxml import html
import xlsxwriter
import webbrowser
from collections import OrderedDict

def main():
    #grab the search params and desired filename
    dict = prompt_user()
    path = raw_input('\n--> Supply a filename to write to [default: auto-generated]: ')

    if len(path) == 0:
        path = None

    # query the site and write to file
    export(dict, path)

    # done

# give option to enter each parameter
def prompt_user():
    dict = OrderedDict ([
        ('FirstName', 'null'),
        ('LastName', 'null'),
        ('City', 'null'),
        ('IsGroupByCity', 'false'),
        ('AptNumber', 'null'),
        ('Street', 'null'),
        ('House', 'null'),
        ('PostalCode', 'null'),
        ('PhoneNumber1', 'null'),
        ('PhoneNumber2', 'null'),
        ('PhoneNumber3', 'null'),
        ('Provinces', ['BC','YT']),
        ('AlternativeName', 'null'),
        ('SortColumnName', 'null')
    ])

    print "Please give search terms or press [return] to use default."
    for each in dict.items():
        input = raw_input("--> %s [default %s]: " % (each[0], each[1]))
        dict[each[0]] = each[1] if (len(input) == 0) else input
    return dict

# allow one or more search keys to be passed to construct a full query from
def make_dict(partial_dict):
    dict = OrderedDict ([
        ('FirstName', 'null'),
        ('LastName', 'null'),
        ('City', 'null'),
        ('IsGroupByCity', 'false'),
        ('AptNumber', 'null'),
        ('Street', 'null'),
        ('House', 'null'),
        ('PostalCode', 'null'),
        ('PhoneNumber1', 'null'),
        ('PhoneNumber2', 'null'),
        ('PhoneNumber3', 'null'),
        ('Provinces', ['BC','YT']),
        ('AlternativeName', 'null'),
        ('SortColumnName', 'null')
    ])

    for each in partial_dict.items():
        dict[each[0]] = each[1]

    return dict

# using using prompt data, create a filename
def generate_filename(dict):
    num = 1

    # files are stored like main st 1.xlsx, main st 2.xlsx
    # this block adds on another , i.e. main st 3.xlsx
    for each in os.listdir('data'):
        if each.startswith(dict['Street']):
            num = int(each[(len(dict['Street']) + 1):-5]) + 1
    filename = "%s %d" % (dict['Street'], num)
    return filename

# format the dictionary to url encoding
def format(dict):
    data = "%7B"
    for key, value in dict.iteritems():
        data += "%22" + key + "%22:"
        if key == 'IsGroupByCity':
            data += value
        elif key == 'Provinces':
            data += "%5B"
            provincecount = 1
            for province in value:
                data += "%22" + province + "%22"
                if provincecount < len(value):
                    data += ","
                provincecount += 1
            data += "%5D"
        else:
            if value != 'null':
                data += "%22" + value + "%22"
            else:
                data += value
        if key != 'SortColumnName':
            data += ","
    data += "%7D"
    return data

# login to site and export data into xlsx
def export(dict, filename=None):
    print "Export Start."
    print "Logging into site."

    if not 'data' in os.listdir('.'):
        os.mkdir('data')

    if filename == None:
        filename = generate_filename(dict)

    # Enter login details here - will add static page to enter details at later point
    username = ""
    password = ""
    domain = ""

    # sign in - https://kazuar.github.io/scraping-tutorial/
    session_requests = requests.session()
    loginurl = domain + "/api/login"
    payload = {'Username': username, 'Password': password}
    result = session_requests.post(loginurl, data = payload)

    print "Exporting search results to data/%s.xlsx" % filename
    exporturl = domain + "/search/export"
    # example payload = {'Data' : "%7B%22FirstName%22:null,%22LastName%22:null,%22City%22:%22Colwood%22,%22IsGroupByCity%22:false,%22AptNumber%22:null,%22Street%22:null,%22House%22:null,%22PostalCode%22:null,%22PhoneNumber1%22:null,%22PhoneNumber2%22:null,%22PhoneNumber3%22:null,%22Provinces%22:%5B%22BC%22,%22YT%22%5D,%22AlternativeName%22:null,%22SortColumnName%22:null%7D"}
    payload = { 'Data' : format(dict) }
    result = session_requests.post(exporturl, data = payload)

    with open("data/%s.xlsx" % filename, "w") as f:
        f.write(result.content)

if __name__ == "__main__":
    main()

# following for testing the search - query string is url encoded

# querystring = "?searchFilters%5BCity%5D=Colwood&searchFilters%5BIsGroupByCity%5D=false&searchFilters%5BProvinces%5D%5B%5D=BC&searchFilters%5BProvinces%5D%5B%5D=YT"
# result = session_requests.get(domain + "/search/api/search" + querystring)
# with open("requests_results.html", "w") as f:
#     f.write(result.content)
# webbrowser.open("requests_results.html")
