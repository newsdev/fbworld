import sys
import json
import os

from fbworld.models import Edge, Member, Group
from fbworld.get_members_dict import create_dict

members_file = sys.argv[1]
groups_file = sys.argv[2]

"""E maps <edge_id>:Edge object>"""
E = {}

def strength(group1, group2):
    return len(set(group1.members).intersection(set(group2.members)))

def add_edge(e):
    if e.id not in E:
        E[e.id] = e.__dict__

def dict_to_group(dict_group):
    return Group(**dict_group)

def compare_groups(member, groups_dict):
    #Search G for group g.
    #If group has not been inspected, add to G
    for g1 in member['groups']:
        member['groups'].remove(g1)
        group1 = dict_to_group(groups_dict.get(str(g1)))

        for g2 in member['groups']:
            group2 = dict_to_group(groups_dict.get(str(g2)))
            #Search E for edge e
            #If edge has not been inspected, add to E
            e = Edge(group1=group1, group2=group2, strength=strength(group1, group2))
            add_edge(e)

if __name__ == '__main__':

    """Get members and groups into dictionaries"""
    members_dict = create_dict(members_file)
    groups_dict = create_dict(groups_file)
    
    """Compare groups of each member"""
    for member in members_dict:
        compare_groups(member, groups_dict)


    """Dump data to json"""
    data = {}
    data['nodes'] = list(groups_dict.keys())
    data['links'] = [E.get(e) for e in E]

    print(data)

    with open("nodes_links.json", 'w') as writefile:
        writefile.write(json.dumps(data))

