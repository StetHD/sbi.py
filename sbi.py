# coding: utf-8

import random
import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from user_agent import generate_user_agent
import requests

# Python 3 compatibility
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


__version__ = '0.0.7'
__all__ = ['search_by', 'SBIResult', 'OhShitCAPTCHA']

GOOGLE_BASE_URL = 'https://www.google.com/'
GOOGLE_SEARCH_BY_ENDPOINT = 'https://images.google.com/searchbyimage?hl=en&image_url='


class OhShitCAPTCHA(Exception):
    """
    Google: You Shall Not Pass!!!
    """
    pass


class SBIResult(object):

    def __init__(self):
        self.result_page = None
        self.all_sizes_page = None
        self.best_guess = None
        self.images = []

    def __bool__(self):
        return bool(self.images)

    __nonzero__ = __bool__

    def __len__(self):
        return len(self.images)

    def __repr__(self):
        # print('self.result_page', self.result_page)
        # print('self.all_sizes_page', self.all_sizes_page)
        return '<SBIResult [best_guess: %s]>' % (self.best_guess)

    def to_dict(self):
        return self.__dict__


def fire_request(url, referer):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'en-us,en;q=0.8,zh-tw;q=0.6,zh;q=0.4',
        'cache-control': 'no-cache',
        'connection': 'close',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': referer,
        'user-agent': generate_user_agent(),
    }

    r = requests.get(url, headers=headers)

    content = r.content

    # print('r.url', r.url)
    print('r.status_code', r.status_code)

    return content


def cook_soup(text):
    soup = BeautifulSoup(text, 'html5lib')

    captcha_input = soup.find_all('input', {'name': 'captcha'})
    if captcha_input:
        raise OhShitCAPTCHA

    return soup


def extract_best_guess(html):
    match = re.search(b'Best guess for this image.*?>(.*?)</a>', html, re.IGNORECASE | re.MULTILINE)

    if match:
        text = match.group(1)
        text = text.title()
    else:
        text = ''

    return text


def search_by(url=None):
    image_url = url

    result_url = GOOGLE_SEARCH_BY_ENDPOINT + image_url

    referer = 'https://www.google.com/imghp'
    result_html = fire_request(result_url, referer)

    if 'Find other sizes of this image' not in result_html:
        print(result_html)

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

    all_sizes_html = fire_request(all_sizes_url, referer=all_sizes_url)

    soup = cook_soup(all_sizes_html)

    img_links = soup.find_all('a', {'class': 'rg_l'})
    images = []
    for a in img_links:
        url = a['href']
        parse_result = urlparse.urlparse(url)

        querystring = parse_result.query
        querystring_dict = urlparse.parse_qs(querystring)

        image = {}
        image['url'] = querystring_dict['imgurl'][0]
        image['width'] = int(querystring_dict['w'][0])
        image['height'] = int(querystring_dict['h'][0])

        images.append(image)

    result.images = images

    return result


from pprint import pprint
result = search_by("https://s3-ap-northeast-1.amazonaws.com/vinta/test/kiko_mizuhara_1.jpg")
pprint(result)
pprint(result.images)
