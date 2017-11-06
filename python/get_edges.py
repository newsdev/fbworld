import sys
import json


"""G_ids is the set of all Group ids. G is the list of all Groups"""
G_ids = set()
G = []

"""E_ids is the set of all Edge ids. E is the list of all Edges"""
E_ids = set()
E = []

def add_edge(e):
    if e.id is not in E_ids:
        E_ids.add(e.id)
        E.append(e)

def add_group(g):
    if g is not in G_ids:
        G_ids.add(g)
        G.append(Group(g, access_token))

def compare_groups(member):
    
    #Search G for group g
    #If group has not been inspected, add to G
    for g in member.groups:
        member.groups.remove(g)
        add_group(g)

        for g2 in member.groups:
            #Search E for edge e
            #If edge has not been inspected, add to E
            e = Edge(g, g2, strength(g, g2))
            add_edge(e)
        


if __name__ == __main__:

"""Get members of txt file into array"""

"""Select member"""
members = set(member.get_groups())
while members != set():
    curr_member = members.pop()
    """Compare groups of each member"""
    compare_groups(curr_member)

"""Dump nodes, edges to json"""
with open("graph.json", 'w') as writefile:
    json.dump(writefile, data)

        
