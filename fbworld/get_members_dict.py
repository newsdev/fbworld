import sys
import json
import os

from fbworld.models import Edge, Member, Group

def main(file_path):

    members_of_groups = {}

    with open(file_path, 'r') as readfile:
        members = list(json.loads(readfile.read())['data'])

    for m in members:
        if m.get('groups', None):
            for g in m['groups']:
                if not members_of_groups.get(g['id'], None):
                    members_of_groups[g['id']] = []

                new_members = Group(**g).get_members()

                for m in new_members:
                    members_of_groups[g['id']].append(m)

                print('get_members_dict.main: adding %s groups to %s.' % (len(new_members), g['id']))


    print("----- THIS WILL BE THE OUTPUT -----")
    for k,v in members_of_groups.items():
        print("group %s has %s members" % (k, len(v)))
    print("----- OUTPUT COMING -----")

    payload = {}
    payload['data'] = members_of_groups
    filename = "%s_groups_output.json" % file_path.split('.txt')[0]

    with open(filename, 'w') as writefile:
        writefile.write(json.dumps(payload))

    print("Success! Groups copied to {}".format(filename))

if __name__ == '__main__':
    file_path = sys.argv[1]
    main(file_path)