import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pprint import pprint
from helpers.merge import merge_monster

with open('exports/03-05-2023/monsters-2023-03-05.json') as f:
    main = json.load(f)

with open('exports/03-11-2023/monsters.json') as f:
    new = json.load(f)

# merge the new monsters into the main monsters
names = set()
unique = []

for monster in main:
    if monster["name"] not in names:
        names.add(monster["name"])
        if "environment" in monster:
            monster["environments"] = monster["environment"]
            del monster["environment"]
        unique.append(monster)
    else:
        for un in unique:
            if un["name"] == monster["name"]:
                un = merge_monster(un, monster)
                break

with open('data/open5e/monsters.json') as f:
    open5e = json.load(f)

# change the environment key to environments
for monster in open5e:
    if "environment" in monster:
        monster["environments"] = monster["environment"]
        del monster["environment"]

pprint(len(open5e))
pprint(len(unique))

# merge unique monsters into open5e by name
res = []
for monster in open5e:
    if monster["name"] in names:
        for un in unique:
            if un["name"] == monster["name"]:
                if "environments" not in monster:
                    monster["environments"] = []
                monster = merge_monster(monster, un)
                break
    res.append(monster)


# filter out monsters with no environments
has_envs = [monster for monster in res if "environments" in monster and len(monster["environments"]) > 0]

pprint(len(has_envs))
# with open('exports/03-11-2023/merged.json', 'w') as f:
#     json.dump(res, f, indent=4)

