# coding: utf-8

import re

# Python 3 compatibility
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from bs4 import BeautifulSoup
import requests


__version__ = '0.0.4'
__all__ = ['search_by', 'SBIResult']


class SBIResult(object):

    def __init__(self):
        self.result_page = None
        self.all_sizes_page = None
        self.best_guess = None
        self.images = []

    def to_dict(self):
        return self.__dict__


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
    'origin': 'http://www.google.com/',
    'referer': 'https://www.google.com/',
}

GOOGLE_BASE_URL = 'http://www.google.com/'
GOOGLE_SEARCH_BY_ENDPOINT = 'http://images.google.com/searchbyimage?hl=en&image_url='


def make_request(url):
    r = requests.get(url, headers=HEADERS)
    content = r.content

    return content


def cook_soup(text):
    soup = BeautifulSoup(text)

    return soup


def extract_best_guess(html):
    match = re.search(b'Best guess for this image.*?>(.*?)</a>', html, re.M)
    text = match.group(1).decode()

    return text.title()


def search_by(url=None, file=None):
    """
    TODO: support file
    """

    image_url = url
    image_file = file

    """
    Search result page
    """

    result_url = GOOGLE_SEARCH_BY_ENDPOINT + image_url

    result_html = make_request(result_url)

    result = SBIResult()
    result.result_page = result_url
    result.best_guess = extract_best_guess(result_html)

    soup = cook_soup(result_html)

    all_sizes_a_tag = soup.find('a', text='All sizes')

    # No other sizes of this image found
    if not all_sizes_a_tag:
        return result

    all_sizes_href = all_sizes_a_tag['href']
    all_sizes_url = urlparse.urljoin(GOOGLE_BASE_URL, all_sizes_href)

    result.all_sizes_page = all_sizes_url

    """
    All sizes page
    """

    all_sizes_html = make_request(all_sizes_url)

    soup = cook_soup(all_sizes_html)

    img_links =  soup.find_all('a', {'class': 'rg_l'})
    images = []
    for a in img_links:
        url = a['href']
        parse_result = urlparse.urlparse(url)

        querystring = parse_result.query
        querystring_dict = urlparse.parse_qs(querystring)

        image = {}
        image['url'] = querystring_dict['imgurl'][0]
        image['width'] = querystring_dict['w'][0]
        image['height'] = querystring_dict['h'][0]

        images.append(image)

    result.images = images

    return result
