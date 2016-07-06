import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export import Export
import route_parser

def test_basic_export():
    ex = Export()
    ex.set_login_details(None, None)
    ex.set_parsed_routes([["SELLECK WAY",[3223]]])
    ex.generate_excel()

def test_parse_export():
    ex = Export()
    ex.set_login_details(None, None)
    parsedroutes = route_parser.parse("4-40 Beach Dr Even#, 650-776 Mountjoy Ave Even#, 2019-2027 Runnymede Ave Odd# (19)")
    ex.set_parsed_routes(parsedroutes)
    ex.generate_excel()    

if __name__=="__main__":
    # test_basic_export()
    test_parse_export()
