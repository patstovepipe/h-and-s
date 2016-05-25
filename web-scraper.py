from flask import Flask, render_template, request
from lxml import html
import requests
import re
import xlwt

app = Flask(__name__)

# Regex used to validate URL - http://codereview.stackexchange.com/questions/19663/http-url-validating
def getregex():
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex

# Write to excel file - http://stackoverflow.com/questions/13437727/python-write-to-excel-spreadsheet
def output(filename, data):
    book = xlwt.Workbook()
    sh = book.add_sheet('Web Scraped Sheet')

    col1_name = 'Column 1'
    col2_name = 'Column 2'

    sh.write(0, 0, col1_name)
    sh.write(0, 1, col2_name)

    for num in range(1, len(data)):
        sh.write(num, 0, data[num - 1])
        if num < len(data):
            sh.write(num, 1, data[num])
        num+=1

    book.save(filename)

@app.route('/')
def default():
    return render_template('default.html')

@app.route('/webscrape', methods=['POST'])
def webscrape():
    url = request.form['url']

    # We check if this is a valid url before doing anything more
    regex = getregex()
    if regex.match(url):
        # Web scraping guide here - http://docs.python-guide.org/en/latest/scenarios/scrape/
        page = requests.get(url)
        tag = request.form['tag']

        try:
            tree = html.fromstring(page.content)
            divs = tree.xpath('//%s/text()' % tag)
        except:
            return render_template('default.html')

        # following turns url into char array
        # htmlrows = list(url)

        output('example.xls', divs)


        return render_template('default.html', htmlrows = divs)
    return render_template('default.html')

if __name__ == '__main__':
    # Make sure to set debug to false for production..
    app.debug = True
    app.run(host='0.0.0.0')
