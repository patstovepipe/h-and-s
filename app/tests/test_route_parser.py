import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import route_parser

def test_basic_export():
    route = "4-40 Beach Dr Even#, 650-776 Mountjoy Ave Even#, 2019-2027 Runnymede Ave Odd# (19)"
    # route = "Pattullo Pl, 900-924 Deal St,2623-2641, 2671 Odd# Margate Ave. 906-999 Newport Ave (35)"
    # route = "737 -975 Linkleas Ave Odd#, 2555, 2575 McNeill Ave Odd #, 2510, 2530 Central Ave Even # (24)"
    route_parser.init(route, None, None, None)

def test_filename():
    filename = "app/tests/test.xlsx"
    route_parser.init(None, filename, None, None)

def terminal():
    args = sys.argv[1:]
    if len(args) == 0:
        route = raw_input("> [route_parser] Insert a route to query with, or nothing to run a test route.] \n \
                           > ")
        if len(args) == 0:
            route = "4-40 Beach Dr Even#, 650-776 Mountjoy Ave Even#, 2019-2027 Runnymede Ave Odd# (19)"
            print "[route_parser] No args provided - Running the following test route: "
            print route
        route_parser.init(route)

if __name__=="__main__":
    test_filename()
