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
    """
    """
    def __init__(self, *args, **kwargs):
        self.value = None
        self.source = None
        self.target = None
        self.id = None
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

        # group1 is the group w the lesser id
        min_id = min(kwargs['group1'].id, kwargs['group2'].id)
        if min_id == kwargs['group1'].id:
            self.source = str(kwargs['group1'].id)
            self.target = str(kwargs['group2'].id)
        else:
            self.source = str(kwargs['group2'].id)
            self.target = str(kwargs['group1'].id)

        self.value = kwargs['strength']
        self.id = self.source + "_" + self.target + "_" + str(self.value)

    def equals(e):
        if e.id == self.id:
            return true


class Member:
    """
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.name = None
        self.administrator = None
        self.groups = None
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)


class Group:
    """
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.name = None
        self.link = None
        self.members = []
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

        if kwargs.get('members', None):
            print("Group has %s members; adding %s members." % (len(self.members), len(kwargs['members'])))
            self.members += kwargs['members']

        if not kwargs.get('members', None):
            self.scrapePageSearch()

    def get_members(self):
        return list(self.members)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "link": self.link, "members": self.members}

    def toJSON(self):
        return json.dumps(self.to_dict())

    def equals(group):
        if group.group_id == self.group_id:
            return True
        return False

    def getGroupMembersUrl(self):
        # Construct the URL string; see http://stackoverflow.com/a/37239851
        url = "https://graph.facebook.com/v2.10/{}/members?access_token={}&debug=all&format=json&method=get&pretty=0&suppress_http_code=1".format(self.id, fbworld.ACCESS_TOKEN)
        return url

    def scrapePageSearch(self):
        print("models.scrapePageSearch: Extracting members of group with id: {}".format(self.id)) 
        has_next_page = True
        num_processed = 0
        url = self.getGroupMembersUrl()

        while has_next_page and url is not None:
            raw = dict(json.loads(request_until_succeed(url)))
            for m in raw['data']:
                self.members.append(m['id'])

             # if there is no next page, we're done.
            if 'paging' in raw and 'next' in raw['paging']:
                url = raw['paging']['next']
            else:
                has_next_page = False

        print("models.scrapePageSearch: Group has {} members".format(str(len(self.members))))
