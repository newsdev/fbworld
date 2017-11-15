import sys
import json
import os

from fb_objects import *

access_token = os.environ.get('INDV_ACCESS_TOKEN', None)
file = sys.argv[1]

"""G maps <group_id>:<Group objects>"""
G = {}

def add_group(id):
    if id not in G:
        group = Group(id)
        G[id] = group.__dict__
        return group
    
def get_groups(member):
    for g in member['groups']:
        add_group(g) 

def create_dict(file):
    with open(file, 'r') as readfile:
        data = json.loads(readfile.read())
        return data['data']

"""G maps <group_id>:<Group objects>"""

if __name__ == '__main__':

    """Get members into dictionary memberid:[groups]"""
    member_dict = create_dict(file)

    """Grab groups for each member"""
    for member in member_dict:
        get_groups(member)

    """Dump dictionary"""
    data = {}
    data['data'] = G
    filename = file + "_groups.json"
    with open(filename, 'w') as writefile:
        json.dump(data, writefile)

