import sys
import json
import os

from fbworld.models import Edge, Member, Group

file_path = sys.argv[1]

"""G maps <group_id>:<Group objects>"""
G = {}
G_list = []
def add_group(g):
    id = g['id']
    if id not in G:
        group = Group(**g)
        print("group initialization members " + str(len(group.members)))
        for key in G.keys():
            print("add_group, each key " + str(len(G.get(key)['members'])))
        G[id] = group.to_dict()
        for key in G.keys():
            print("add_group, each key 2" + str(len(G.get(key)['members'])))
        print("add_group " + str(len(G[id]['members'])))
        return group
    
def get_groups(member):
    for g in member['groups']:
        add_group(g) 
        #HERE th
        for key in G.keys():
            print("get_groups " + str(len(G.get(key)['members'])))

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
#HERE the groups all have 902 members
    for key in G.keys():
        print(len(G.get(key)['members']))

    """Dump dictionary"""
    data = {}
    data['data'] = G
    data['data_list'] = G_list
    filename = file_path + "_groups.json"
    with open(filename, 'w') as writefile:
        json.dump(data, writefile)
    print("Success! Groups copied to {}".format(filename))

