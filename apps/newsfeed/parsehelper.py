import re, requests
from bs4 import BeautifulSoup as bs

"""
This function is to parse out content using a regular expression pattern from a string.
<param>regex_pattern</param>
<param>string</param>
"""

def parse_definition(regex_pattern, string):
    result = re.compile(regex_pattern, flags=re.MULTILINE|re.DOTALL)
    # Checking if the patten works for the string
    if not result.search(string):
        return "None"
    else:
        output = clean_html(result.search(string).group(1))
        return output

def get_page(url):
    return requests.get(url)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_bleacher_report_body_text(url):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    article_body = soup.find('div', attrs={'class':'organism contentStream'}).text.replace(u'\xa0',u'')
    return article_body

def get_reporter_name(reporter, regex=None):
    if reporter is None:
        return None
    if regex is not None:
        reporter = re.sub(regex, '', reporter).strip()
    reporter_dict = {}
    reporter = reporter.split()
    if len(reporter) <= 3:
        reporter_dict['first_name'] = reporter[0]
        reporter_dict['last_name'] = reporter[len(reporter)-1]
    else:
        reporter_dict['first_name'] = reporter
    return reporter_dict
