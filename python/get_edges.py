import sys
import json


"""G_ids is the set of all Group ids. G is the list of all Groups"""
G_ids = set()
G = []

"""E_ids is the set of all Edge ids. E is the list of all Edges"""
E_ids = set()
E = []

def compare_groups(member):

    for g in member.groups:
        member.groups.remove(g)
        if g.id is not in G_ids:
            G_ids.add(g.id)
            G.append(G)
        for g2 in member.groups:
            e = Edge(g, g2, strength(g, g2))
            if e.id is not in E_ids:
                E_ids.add(e.id)
                E.append(e)
        
#Search G for group g
#If group has not been inspected, add to G

#Search E for edge e
#If edge has not been inspected, add to E

if __name__ == __main__:

"""Get members of txt file into array"""

"""Select member"""
member_groups = set(member.get_groups())
while member_groups != set():
    curr_member = member_groups.pop()
    """Compare groups of each member"""
    compare_groups(curr_member)

"""Dump nodes, edges to json"""
with open("graph.json", 'w') as writefile:
    json.dump(writefile, data)

        
