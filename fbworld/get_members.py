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

from fbworld.models import Edge, Member, Group
from fbworld.utils import request_until_succeed, unicode_decode

"""Access token from environment"""
print(fbworld.ACCESS_TOKEN)

"""Class used to query for a set of groups"""
def get_group_ids(f):
    with open(f, 'r') as file:
        groups = file.readlines()

    groups = [x.strip("\n") for x in groups]    
    return groups

if __name__ == '__main__':

    """Get set of all politicized groups"""
    clinton_groups = get_group_ids("hillary_clinton_groups.txt")
    trump_groups = get_group_ids("donald_trump_groups.txt")
    sanders_groups = get_group_ids("bernie_sanders_groups.txt")
    all_groups_set = set(trump_groups).union(clinton_groups).union(sanders_groups) 

    """Get all members of all politicized groups"""
    all_members_set = set()
    num_groups = len(all_groups_set)
    curr_group = 1
    for group in all_groups_set:
        print("\nScraping group {} out of {}".format(str(curr_group), str(num_groups)))
        all_members_set = all_members_set.union(set(Group(group).members))
        print("Number of members collected: {}\n".format(str(len(all_members_set))))
        curr_group += 1

    """Write member ids to file"""
    with open("all_members.txt", 'w') as writefile:
        for member in all_members_set:
            writefile.write(member.id + "\n")


