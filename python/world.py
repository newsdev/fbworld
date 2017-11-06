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
access_token = os.environ.get('INDV_ACCESS_TOKEN', None) 
print(access_token)

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
    with open(f, 'r') as file:
        groups = file.readlines()

    groups = [x.strip("\n") for x in groups]    
    return groups

if __name__ == '__main__':

    """Get set of all politicized groups"""
    clinton_groups = extract_groups("hillary_clinton_groups.txt")
    trump_groups = extract_groups("donald_trump_groups.txt")
    sanders_groups = extract_groups("bernie_sanders_groups.txt")
    all_groups_set = set(trump_groups).union(clinton_groups).union(sanders_groups) 

    """Get all members of all politicized groups"""
    all_members_set = set()
    num_groups = len(all_groups_set)
    curr_group = 1
    for group in all_groups_set:
        print("\nScraping group {} out of {}".format(str(curr_group), str(num_groups)))
        all_members_set = all_members_set.union(set(Group_Members(group, access_token).members))
        print("Number of members collected: {}\n".format(str(len(all_members_set))))
        curr_group += 1
    with open("all_members.txt", 'w') as writefile:
        for member in all_members_set:
            writefile.write(member.id + "\n")


