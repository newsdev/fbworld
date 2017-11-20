import json
import sys
import os

directory = sys.argv[1]

script = {}
script["apiVersion"] = "v1"
script["kind"] = "List"
items = []

"""Download all txts into list"""
list_lists = []
n = 0
for txt in os.listdir(directory):
    if txt.endswith(".txt"):
        with open(directory + "/" + txt, 'r') as f: 
            list_lists.append([line.strip() for line in f]) 
            n += 1
        
"""Set up script"""
for i in range(n):

    pod = {}
    pod["kind"] = "Pod"
    pod["apiVersion"] = "v1"
    pod["metadata"] = {"name":"fbtest-{}".format(str(i))}
    pod["spec"] = {}
    pod["spec"]["containers"] = []

    container = {}
    container["name"] = "container-{}".format(str(i))
    container["image"] = "duckduckgo"
    container["command"] = ["scrape-facebook/try-docker-electron/docker-compose", "run", "electron", "bash", "|", "node", "scrape-facebook/try-docker-electron/index.js"]
    container["env"] = {}
    container["env"]["name"] = "USER_IDS"
    container["env"]["value"] = ",".join(list_lists[i])
    #container["command"] = ["python", "fbworld/fbworld/get_member_dict.py", "{}.txt".format(str(i))]

    pod["spec"]["containers"].append(container)
    items.append(pod) 

"""Write script to json"""
script["items"] = items
with open("fbtest.json", "w") as f:
    json.dump(script, f, indent=4)

print("Success! Wrote fbtest.json")
