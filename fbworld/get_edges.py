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
        print(g1['id'])
        dict = groups_dict.get(g1['id'])
        group1 = Group(**dict)
        member['groups'].remove(g1)

        for g2 in member['groups']:
            group2 = dict_to_group(groups_dict.get(g2))
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
    data['nodes'] = [{'id':g, 'size':len(groups_dict.get(g)['members'])} for g in groups_dict]
    data['links'] = [E.get(e) for e in E]

    with open("nodes_links.json", 'w') as writefile:
        writefile.write(json.dumps(data))

    print("Success! Wrote nodes and links to nodes_links.json")

