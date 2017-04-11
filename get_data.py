import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import requests

UTF8 = 'utf-8'
USERAGENT = """Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"""
httpHeaders = {'User-Agent': USERAGENT,
               'Accept': "application/json, text/javascript, text/html,*/*",
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Accept-Language': 'en-US,en;q=0.8'
               }


url = 'http://www.baseball-reference.com/leagues/MLB/2016-schedule.shtml'

req = requests.get(url.encode(UTF8), headers=httpHeaders)
html = req.text

query = '<p class="game">.+?<a href=".+?">(.+?)</a>.+?\((.+?)\).+?'\
        '<a href=".+?">(.+?)</a>.+?\((.+?)\).+?</p>'

data_dict = {}
data_dict['away_team'] = []
data_dict['away_score'] = []
data_dict['home_team'] = []
data_dict['home_score'] = []

for match in re.compile(query, re.DOTALL).finditer(html):
    data_dict['away_team'].append(match.group(1))
    data_dict['away_score'].append(int(match.group(2)))
    data_dict['home_team'].append(match.group(3))
    data_dict['home_score'].append(int(match.group(4)))

df = pd.DataFrame.from_dict(data_dict)
df.to_pickle('./2016_scores.pkl')
