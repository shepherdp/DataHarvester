# Data harvesting functions for KY.

'''
Data to harvest:
    UCC
    Paycheck Protection
    BBB
'''

from bs4 import BeautifulSoup
import urllib.request
import requests
import os


def get_ky_ucc_filings_text():
    # Note: KY website URL updates dynamically.  Need to grab a fresh URL when running this function.
    url = 'https://web.sos.ky.gov/ftucc/(S(0cy0tki0pq1io4rtte20pzcr))/search.aspx'

    # The boilerplate here remains hard-coded.  Only need to change the search term.
    data = {"ctl00$ContentPlaceHolder1$SearchForm1$tOrgname": 'ab',
            "ctl00$ContentPlaceHolder1$SearchForm1$bSearch": 'Search',
            "__VIEWSTATE": "/wEPDwUJMzQ1MjYzMTk4D2QWAmYPZBYCAgkPZBYCAgEPZBYEAgsPDxYCHgdWaXNpYmxlaGRkAg0PDxYCHwBoZGRk7+hUvc+Nf6LnERebHeOfhLsHmM0V6wPZ4kvvWfmPR1Q=",
            "__VIEWSTATEGENERATOR": "90EF923B",
            "__EVENTVALIDATION": "/wEdAAttTUHueSDf0taGo+AaqBOqLMwDBQbKz92Q549SXLXbuD6jwHdsd0xXMZV00FTIVczkNMK+90Ic77EqUA9zsCFm2ieFdJTbE4kzWBKcjtdLG6CMFUghtyCH9lsHjL1EFhzdxn/JBfahsDfW+UpblqA3FkkLbwPePhE13/FRLcmQBRcWugM+JRBsmB0ElzvmIrZoMag/3HBeJB9AhAIKR9lohacLQsSR/wCMATepgD6QmmFl4Z08FauHcJ/v+DTsqNHxrSwIorsfckMLkUNTx7x3"}

    response = None
    with requests.session() as s:
        s.get(url)
        response = s.post(url, data=data)
    return response.text


def get_ky_ucc_filings_entries():
    text = get_ky_ucc_filings_text()
    soup = BeautifulSoup(text, 'html.parser')

    result = []

    # This grabs all of the table rows from the search results.
    rows = soup.findAll('tr', {'class': 'Activebg'})

    for r in rows:
        row = []
        children = r.findChildren('td')
        for child in children:
            text = child.text.replace(',', '')
            row.append(text)
        result.append(row)

    return result


def write_results(filename, data):
    cwd = os.getcwd()
    datadir = os.path.join(cwd, 'Data')
    if not os.path.exists(datadir):
        os.mkdir(datadir)
    filename = os.path.join(datadir, filename)
    with open(filename, 'w') as f:
        f.write('Name,Filing Number,File Date,Lapse Date,Secured Party\n')
        for row in data:
            line = ''
            for item in row:
                line += item + ','
            f.write(line[:-1] + '\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    result = get_ky_ucc_filings_entries()
    write_results('testdata.csv', result)
