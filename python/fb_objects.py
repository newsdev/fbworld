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

access_token = os.environ.get('INDV_ACCESS_TOKEN')

class Edge:
    def __init__(self, group1, group2, strength):
        """group1 is the group w the lesser id"""
        min_id = min(group1.id, group2.id)
        if min_id == group1.id:
            self.source = group1
            self.target = group2
        else:
            self.source = group2
            self.target = group1

        self.value = strength
        self.id = str(self.source.id) + "_" + str(self.target.id) + "_" + str(value)

    def equals(e):
        if e.id == self.id:
            return true
        
class Member:
    def __init__(self, id, name, administrator, groups):
        self.id = id
        self.name = name
        self.administrator = administrator
        self.groups = groups

class Group:

    def __init__(self, group_id, name = '', link = '', members = []):
        self.id = group_id
        self.name = name
        self.link = link
        self.members = members
        if (self.members == []) {
            self.scrapePageSearch()
        }

    def toJSON(self):
        return json.dumps(self, default=lambda o:  o.__dict__,
            sort_keys=True, indent=4)

    def equals(group):
        if group.group_id == self.group_id:
            return true

    def getGroupMembersUrl(self):

        # Construct the URL string; see http://stackoverflow.com/a/37239851 for
        url = "https://graph.facebook.com/v2.10/{}/members?access_token={}&debug=all&format=json&method=get&pretty=0&suppress_http_code=1".format(self.id, access_token)
        return url

    def scrapePageSearch(self):
        print("Extracting members of group with id: {}".format(self.id)) 
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

