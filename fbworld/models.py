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

import fbworld
from fbworld.utils import request_until_succeed, unicode_decode


class Edge:
    value = None
    source = None
    target = None
    id = None
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

        """group1 is the group w the lesser id"""
        min_id = min(kwargs['group1'].id, kwargs['group2'].id)
        if min_id == kwargs['group1'].id:
            self.source = kwargs['group1'].__dict__
            self.target = kwargs['group2'].__dict__
        else:
            self.source = kwargs['group2'].__dict__
            self.target = kwargs['group1'].__dict__

        self.value = kwargs['strength']
        self.id = str(self.source['id']) + "_" + str(self.target['id']) + "_" + str(self.value)

    def equals(e):
        if e.id == self.id:
            return true


class Member:
    id = None
    name = None
    administrator = None
    groups = None

    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)


class Group:
    id = None
    name = None
    link = None
    members = []

    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

        self.scrapePageSearch()

    def toJSON(self):
        return json.dumps(self, default=lambda o:  o.__dict__,
            sort_keys=True, indent=4)

    def equals(group):
        if group.group_id == self.group_id:
            return True
        return False

    def getGroupMembersUrl(self):
        # Construct the URL string; see http://stackoverflow.com/a/37239851 for
        url = "https://graph.facebook.com/v2.10/{}/members?access_token={}&debug=all&format=json&method=get&pretty=0&suppress_http_code=1".format(self.id, fbworld.ACCESS_TOKEN)
        print(url)
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

