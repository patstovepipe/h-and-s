import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export import Export

def test_basic_export():
    ex = Export()
    ex.set_login_details("","")
    searchdict = {"City" : "Colwood"}
    ex.set_search_dict(searchdict)
    ex.generate_excel()

def terminal():
    #grab the search params and desired filename
    searchdict = prompt_user()
    path = raw_input('\n--> Supply a filename to write to [default: auto-generated]: ')

    if len(path) == 0:
        path = None

    # query the site and write to file
    export(searchdict, path)
    # done

# give option to enter each parameter
def prompt_user():
    searchdict = get_dict()

    print "Please give search terms or press [return] to use default."
    for each in searchdict.items():
        input = raw_input("--> %s [default %s]: " % (each[0], each[1]))
        searchdict[each[0]] = each[1] if (len(input) == 0) else input
    return searchdict

if __name__=="__main__":
    test_basic_export()

# following for testing the search - query string is url encoded

# querystring = "?searchFilters%5BCity%5D=Colwood&searchFilters%5BIsGroupByCity%5D=false&searchFilters%5BProvinces%5D%5B%5D=BC&searchFilters%5BProvinces%5D%5B%5D=YT"
# result = session_requests.get(domain + "/search/api/search" + querystring)
# with open("requests_results.html", "w") as f:
#     f.write(result.content)
# webbrowser.open("requests_results.html")
