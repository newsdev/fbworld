import argparse
import csv
import datetime
import json
import os
import sys
import time

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from utils import request_until_succeed, unicode_decode

access_token = os.environ.get('INDV_ACCESS_TOKEN', None) 

arguments = sys.argv[1:]
query = "%20".join(arg for arg in arguments)
query_title = "_".join(arg for arg in arguments)
query_space = " ".join(arg for arg in arguments)

def getGroupSearchUrl():

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    return "https://graph.facebook.com/v2.10/search?q={}&type=group&access_token={}&debug=all&format=json&method=get&pretty=0&suppress_http_code=1".format(query, access_token)

def scrapePageSearch(access_token):
    all_groups = []
    with open('data/{}_groups.txt'.format(query_title), 'w') as file:
        has_next_page = True
        num_processed = 0
        scrape_starttime = datetime.datetime.now()

        print("Scraping groups relevant to {}: {}\n".format(query_space, scrape_starttime))
        url = getGroupSearchUrl()

        while has_next_page and url is not None:
            raw = dict(json.loads(request_until_succeed(url)))
            groups = [{"id":group['id'], "name":group['name']} for group in raw['data']]
            all_groups += groups

            # if there is no next page, we're done.
            if 'paging' in raw:
                url = raw['paging']['next']
            else:
                has_next_page = False

        file.write(json.dumps({"data":all_groups}))


if __name__ == '__main__':
    scrapePageSearch(access_token)
