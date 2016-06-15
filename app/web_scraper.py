from flask import Flask, render_template, request, redirect, url_for
from lxml import html
import requests
import re
import xlwt
import os
from werkzeug import secure_filename
import route_parser

app = Flask(__name__)

# Upload path for the xlsx files
app.config["UPLOAD_FOLDER"] = os.path.abspath(os.curdir) + "/uploads"

# We will be accpeting files with a xlsx extension
app.config["ALLOWED_EXTENSIONS"] = set(['xlsx'])

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

# Check whether the uploaded file is of type "xlsx"
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    uploaded_file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(uploaded_file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(uploaded_file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for("/"))
    return redirect(url_for("/"))

if __name__ == '__main__':
    # Make sure to set debug to false for production..
    app.debug = True
    app.run(host='0.0.0.0')