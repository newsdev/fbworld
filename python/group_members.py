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

class Member:
    def __init__(self, id, name, administrator):
        self.id = id
        self.name = name
        self.administrator = administrator

class Group_Members:

    def __init__(self, group_id, access_token):
        self.group_id = group_id
        self.access_token = access_token 
        self.members = []
        self.scrapePageSearch()

    def getGroupMembersUrl(self):

        # Construct the URL string; see http://stackoverflow.com/a/37239851 for
        url = "https://graph.facebook.com/v2.10/{}/members?access_token={}&debug=all&format=json&method=get&pretty=0&suppress_http_code=1".format(self.group_id, self.access_token)
        return url

    def scrapePageSearch(self):
        print("Extracting members of group with id: {}".format(self.group_id)) 
        has_next_page = True
        num_processed = 0
        url = self.getGroupMembersUrl()

        while has_next_page and url is not None:
            print(".")
            raw_members = json.loads(request_until_succeed(url))

            for raw_member in raw_members['data']:
                self.members.append(raw_member['id'])

             # if there is no next page, we're done.
            if 'paging' in raw_members and 'next' in raw_members['paging']:
                url = raw_members['paging']['next']
            else:
                has_next_page = False

