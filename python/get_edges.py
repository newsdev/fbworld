import sys
import json
import os

from fb_objects import *

access_token = os.environ.get('INDV_ACCESS_TOKEN', None)

"""G maps <group_id>:<Group object>"""
G = {} 

"""E_ids is the set of all Edge ids. E is the list of all Edges"""
E_ids = set()
E = []

def get_members():
    with open('some.txt', 'r') as readfile:
        data = json.loads(readfile.read())
        return data['data']

def add_edge_2(g1, g2, strength):
    min_id = min(g1.id, g2.id)
    max_id = max(g1.id, g2.id)
    edge = str(min_id) + "," + str(max_id) + "," + str(strength)
    E_ids.add(edge)

def add_edge(e):
    if e.id not in E_ids:
        E_ids.add(e.id)
        E.append(e)

def add_group(g):
    if g not in G:
        group = Group(g, access_token)
        G[g] = group
        return group

    else:
        return G.get(g)

def strength(group1, group2):
    return len(set(group1.members).intersection(set(group2.members)))

def compare_groups(member):
    
    #Search G for group g
    #If group has not been inspected, add to G
    for g1_id in member['groups']:
        member['groups'].remove(g1_id)
        group1 = add_group(g1_id)

        for g2_id in member['groups']:
            group2 = add_group(g2_id)
            #Search E for edge e
            #If edge has not been inspected, add to E
            e = Edge(group1, group2, strength(group1, group2))
            #add_edge(e)
            add_edge_2(group1, group2, strength(group1, group2))
        


if __name__ == '__main__':

    """Get members groups into dictionary"""
    member_dict = get_members()   

    """Compare groups of each member"""
    for member in member_dict:
        compare_groups(member)

    """Dump nodes, edges to json"""
    data = {}
    data['groups'] = list(G.keys())
    data['edges'] = list(E_ids)
    print(data)

    with open("graph.json", 'w') as writefile:
        json.dump(data, writefile)

        
