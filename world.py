import argparse
import csv
import datetime
import json
import os
import sys
import time
from group_members import *

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from utils import request_until_succeed, unicode_decode

"""Access token from environment"""
access_token = os.environ.get('INDV_APP_TOKEN', None) 

"""Class representing a group"""
class Group:
        
    def __init__(id, name, members):
        self.id = id
        self.name = name
        self.members = members

"""Class representing a member of a group"""
class Member:
    
    def __init__(id, name, groups):
        self.id = id
        self.name = name
        self.groups = groups
        

"""Class used to query for a set of groups"""
def extract_groups(f):
    groups = []
    with open(f, 'r') as csvfile:
        groups = list(csv.DictReader(csvfile))
    
    group_ids = []
    for group in groups:
        group_ids.append(group['id'])
    return group_ids

if __name__ == '__main__':

    """Get set of all politicized groups"""
    trump_groups = extract_groups("group_csvs/donald_trump_groups.csv")
    clinton_groups = extract_groups("group_csvs/hillary_clinton_groups.csv")
    sanders_groups = extract_groups("group_csvs/bernie_sanders_groups.csv")
    all_groups_set = set(trump_groups).update(clinton_groups).update(sanders_groups)

    """Get all members of all politicized groups"""
    all_members_set = set()
    num_groups = len(all_groups_set)
    curr_group = 0
    for group in all_groups_set:
        print("Done with {} groups out of {}".format(str(curr_group), str(num_groups)))
        all_members_set.add(Group_Members(group, access_token))
        curr_group += 1
        


