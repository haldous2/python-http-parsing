
"""

 Page scraper using BeautifulSoup

 Note: I could go on an on an on scraping a page - I get the jist, this page is a works in progress - not completed
       Got stuck at grabbing two td's - thinking of using the td class instead 'promptTextBox', 'promptElementText'

       Must finish homework, come back to this...

"""

import re, requests
from BeautifulSoup import BeautifulSoup

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
    print "elem.name=%s" % elem.name
    is_tr = elem.name == 'tr'
    td_children = elem.findAll('td', recursive=False)
    has_two = len(td_children) == 2
    #print "is_tr %s, has_two %s" % (is_tr, has_two)
    return is_tr and has_two

def parse_business(parsed):

    ## Display first td with id contentcol
    content_col = parsed.find("td", id="contentcol")
    #print "content_col.type %s" % type(content_col)
    #print content_col.prettify(encoding=encoding)

    ## Display all divs with id like PR[digits]
    id_finder = re.compile(r'PR[\d]+~')
    #return html.find_all('div', id=id_finder)
    data_list = content_col.findAll('div', id=id_finder)
    #print data_list[0].prettify()

    ## Find all trs
    data_tr = data_list[0].findAll('tr')

    data_td = []
    for trs in data_tr:

        ## Now find all trs where two tds exist
        print "%s......" % (trs.name)
        has_two = trs.findAll(has_two_tds, recursive=False)
        #if has_two:
        #    print "has two!!"
        #else:
        #    print "these are not the droids you want"

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
