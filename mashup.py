
"""

 Page scraper using BeautifulSoup

 Note: I could go on an on an on scraping a page - I get the jist, this page is a works in progress - not completed
       Got stuck at grabbing two td's - thinking of using the td class instead 'promptTextBox', 'promptElementText'

       Must finish homework, come back to this...

"""

import re, requests
from BeautifulSoup import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Health inspections reports.')
parser.add_argument('-s', '--score', default='highestscore', help='highestscore (default) or mostinspections')
parser.add_argument('-m', '--map', default=25, help='number of points to map - default is 25')
parser.add_argument('-o', '--order', default='forward', help='forward (default) or backwards')
args = parser.parse_args()

#print "args: %s %s %s" % (args.score, args.map, args.order)

#http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx?Zip_Code=98103

INSPECTION_DOMAIN = "http://info.kingcounty.gov"
INSPECTION_PATH = "/health/ehs/foodsafety/inspections/Results.aspx"

INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'H'
}

def get_inspection_page(**kwargs):

    url = INSPECTION_DOMAIN + INSPECTION_PATH

    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val

    resp = requests.get(url, params=params)
    resp.raise_for_status() # Check for error http 4xx, 5xx

    return resp.content, resp.encoding

def parse_source(html, encoding='utf-8'):
    try:
        # Version 4
        parsed = BeautifulSoup(html, from_encoding=encoding)
    except TypeError:
        # Version 3
        parsed = BeautifulSoup(html, fromEncoding=encoding)
    return parsed

def load_inspection_page(name):

    with open(name, 'r') as fh:
        content = fh.read()
        return content, 'utf-8'

def has_two_tds(elem):
    # If I pass a tr elem in, by the time it gets here it's a td.. weird
    # so... not using this right now
    is_tr = elem.name == 'tr'
    td_children = elem.findAll('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two

def parse_business(parsed):

    ## Display first td with id contentcol
    content_col = parsed.find("td", id="contentcol")

    ## Display all divs with id like PR[digits]
    id_finder = re.compile(r'PR[\d]+~')
    data_list = content_col.findAll('div', id=id_finder)

    ## Find all trs
    data_tr = data_list[0].findAll('tr')

    data_td = []
    for trs in data_tr:

        ## Now find all trs where two tds exist
        if trs.name == "tr":
            td_children = trs.findAll('td', recursive=False)
            if len(td_children) == 2:

                for tds in td_children:
                    print tds

        #for tds in data_td_hastwo:
        #    print "%s ......" % tds
        #    data_td.append(tds)

    for tds in data_td:
        print tds

if __name__ == '__main__':

    qryCol = {'Zip_Code':'98103', 'Business_Name':'a'}

    ## Content from remote or file
    #content, encoding = get_inspection_page(**qryCol)
    content, encoding = load_inspection_page('kingcounty.htm')
    #print content
    #print encoding

    ## Parse content down to business and inspection
    parsed = parse_source(content, encoding)
    #print parsed.prettify(encoding=encoding)
    parse_business(parsed)

    #html, encoding = load_inspection_page('inspection_page.html')
    #parsed = parse_source(html, encoding)
    #content_col = parsed.find("td", id="contentcol")
    #data_list = restaurant_data_generator(content_col)
    #print data_list[0].prettify()
