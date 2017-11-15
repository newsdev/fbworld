import sys
import json
import os

from fbworld.models import Edge, Member, Group

file_path = sys.argv[1]

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

def create_dict(file_path):
    with open(file_path, 'r') as readfile:
        data = json.loads(readfile.read())
        return data['data']

"""G maps <group_id>:<Group objects>"""

if __name__ == '__main__':

    """Get members into dictionary memberid:[groups]"""
    member_dict = create_dict(file_path)

    """Grab groups for each member"""
    for member in member_dict:
        get_groups(member)

    """Dump dictionary"""
    data = {}
    data['data'] = G
    filename = file_path + "_groups.json"
    with open(filename, 'w') as writefile:
        json.dump(data, writefile)

