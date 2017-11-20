import json

n = 2
script = {}
script["apiVersion"] = "v1"
script["kind"] = "List"
items = []
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
    #container["command"] = ["python", "fbworld/fbworld/get_member_dict.py", "{}.txt".format(str(i))]

    pod["spec"]["containers"].append(container)
    items.append(pod) 

script["items"] = items
with open("fbtest.json", "w") as f:
    json.dump(script, f, indent=4)
