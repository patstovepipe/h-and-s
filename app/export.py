import os
import sys
import requests
from lxml import html
import xlsxwriter
import webbrowser
from collections import OrderedDict

class _LoginDetails:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Export:
    def __init__(self):
        self.logindetails = None
        self.filename = None
        self.searchdict = None
        self.domain = ""

    def generate_excel(self):
        self._check_directory()
        self._check_filename()
        session_requests = requests.session()
        result = self._login(session_requests)
        print "After login."
        self._export_to_file(session_requests, result)

    def _check_directory(self):
        if not 'data' in os.listdir('.'):
            os.mkdir('data')

    def _check_filename(self):
        if self.filename == None:
            self.filename = Export._generate_filename(self.searchdict)

    @staticmethod
    def _generate_filename(searchdict):
        num = 1
        # files are stored like main st 1.xlsx, main st 2.xlsx
        # this block adds on another , i.e. main st 3.xlsx
        for each in os.listdir('data'):
            if each.startswith(searchdict['Street']):
                num = int(each[(len(searchdict['Street']) + 1):-5]) + 1
        filename = "%s %d" % (searchdict['Street'], num)
        return filename

    def set_search_dict(self, parsed_routes):
        self.searchdict = Export._searchdict(parsed_routes)

    def set_login_details(self, username, password):
        self.logindetails = _LoginDetails(username, password)

    def _login(self, session_requests):
        loginurl = self.domain + "/api/login"
        payload = {'Username': self.logindetails.username, 'Password': self.logindetails.password}
        return session_requests.post(loginurl, data = payload)

    def _export_to_file(self, session_requests, result):
        exporturl = self.domain + "/search/export"
        payload = { 'Data' : Export._formatdict(self.searchdict) }
        result = session_requests.post(exporturl, data = payload)
        print "Exporting search results to data/%s.xlsx" % self.filename

        with open("data/%s.xlsx" % self.filename, "w") as f:
            f.write(result.content)

    @staticmethod
    def _emptydict():
        return OrderedDict ([
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

    @staticmethod
    def _searchdict(parsed_routes):
        searchdict = Export._emptydict()

        for each in parsed_routes.items():
            searchdict[each[0]] = each[1]

        return searchdict

    # format the search dictionary to url encoding
    @staticmethod
    def _formatdict(searchdict):
        data = "%7B"
        for key, value in searchdict.iteritems():
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
