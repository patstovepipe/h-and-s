import os
import sys
import requests
from lxml import html
import xlsxwriter
import webbrowser
from collections import OrderedDict
from xlrd import open_workbook
import xlwt
import time

class _LoginDetails:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.domain = None

class Export:
    def __init__(self):
        self.logindetails = None
        self.filename = 'results'
        self.searchdict = None
        self.parsedroutes = None

    def generate_excel(self):
        if self.logindetails.username != None and self.logindetails.password != None and self.logindetails.domain != None:
            self._check_directory()
            with requests.session() as s:
                self._login(s)
                print ("After login.")
                self._process_routes(s)
            self.filename = None
        else:
            print "Login details are missing or incomplete."

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

    def set_parsed_routes(self, parsedroutes):
        self.parsedroutes = parsedroutes

    def _set_search_dict(self, parsedroute):
        self.searchdict = Export._searchdict(parsedroute)

    def set_login_details(self, username, password):
        self.logindetails = _LoginDetails(username, password)

    def _login(self, session_requests):
        loginurl = self.logindetails.domain + "/api/login"
        payload = {'Username': self.logindetails.username, 'Password': self.logindetails.password}
        session_requests.post(loginurl, data = payload)

    def _export_to_file(self, session_requests):
        exporturl = self.logindetails.domain + "/search/export"
        payload = { 'Data' : Export._formatdict(self.searchdict) }
        result = session_requests.post(exporturl, data = payload)

        print "Exporting search results to data/%s.xlsx" % self.filename
        # print result.content

        with open("data/%s.xlsx" % self.filename, "wb") as f:
            for chunk in result.iter_content(chunk_size=1024):
                f.write(chunk)

    def _process_routes(self, session_requests):
        filtereddictlist = []
        for route in self.parsedroutes:
            if route == []:
                continue
            self._set_search_dict({ "Street": route[0] })
            self._export_to_file(session_requests)

            dictlist = []
            dictlist = Export._getlistfromworkbook('data/%s.xlsx' % self.filename)
            dictlist = Export._filterdictlist(route[1], dictlist)
            filtereddictlist.extend(dictlist)

            print filtereddictlist

            time.sleep(5)
        Export._writetofile('data/export.xlsx', filtereddictlist)

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

    @staticmethod
    def _resultsdict():
        return OrderedDict ([
            ('Details', None),
            ('Name', None),
            ('House', None),
            ('Street', None),
            ('Apt', None),
            ('City', None),
            ('Prov', None),
            ('Postal', None),
            ('Phone', None)
        ])

    @staticmethod
    def _getlistfromworkbook(filename):
        wb = open_workbook(filename)
        s = wb.sheet_by_index(0)

        num_cols = s.ncols
        resultsdictlist = []
        for row_idx in range(0, s.nrows):
            resultsdict = Export._resultsdict()
            for col_idx, key in zip(range(0, num_cols), resultsdict):
                cell_obj = s.cell(row_idx, col_idx)
                # print cell_obj.value
                resultsdict[key] = cell_obj.value
            resultsdictlist.append(resultsdict)

        return resultsdictlist

    @staticmethod
    def _filterdictlist(housenums, listtofilter):
        housenums = [str(x) for x in housenums]
        return [x for x in listtofilter if x['House'] in housenums]

    @staticmethod
    def _writetofile(filename, dictlist):
        book = xlwt.Workbook()
        sh = book.add_sheet('Sheet1')

        col_names = Export._resultsdict()
        for idx, key in zip(range(0, len(col_names)), col_names):
            sh.write(0, idx, key)

        for row_idx in range(0, len(dictlist)):
            for col_idx, key in zip(range(0, len(dictlist[row_idx])), dictlist[row_idx]):
                sh.write(row_idx + 1, col_idx, dictlist[row_idx][key])

        book.save(filename)
