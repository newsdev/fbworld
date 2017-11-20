import json
import sys

txts = sys.argv[1:]
n = len(txts)

script = {}
script["apiVersion"] = "v1"
script["kind"] = "List"
items = []

"""Download all txts into list"""
list_lists = []
for txt in txts:
    with open(txt, 'r') as f: 
       list_lists.append([line.strip() for line in f]) 

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
    container["environment"] = ",".join(list_lists[i])
    #container["command"] = ["python", "fbworld/fbworld/get_member_dict.py", "{}.txt".format(str(i))]

    pod["spec"]["containers"].append(container)
    items.append(pod) 

"""Write script to json"""
script["items"] = items
with open("fbtest.json", "w") as f:
    json.dump(script, f, indent=4)
