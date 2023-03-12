import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import datetime
from pprint import pprint
from helpers.compare import name_is_similar

with open('data/open5e/monsters.json') as f:
    monsters5e = json.load(f)

with open('data/dnd_beyond/dnd_beyond.json') as f:
    envs = json.load(f)

# dnd_beyond data has duplicate monsters
# so we need to merge them into a single monster
names = set()
unique = []

for monster in envs:
    if monster["name"] not in names:
        names.add(monster["name"])
        # convert environments to a set to remove duplicates
        # if its a list convert it to a set
        if isinstance(monster["environments"], list):
            monster["environments"] = set(monster["environments"])
        # else if its a string convert it to a set
        elif isinstance(monster["environments"], str):
            monster["environments"] = {monster["environments"]}
        unique.append(monster)
    else:
        for un in unique:
            if name_is_similar(un["name"], monster["name"]):
                un["environments"] = un["environments"].union(monster["environments"])
                break

# convert each environment back to a list
for monster in unique:
    monster["environments"] = list(monster["environments"])

# merge open5e monsters with dnd_beyond monsters
for monster5e in monsters5e:
    for monster in unique:
        if name_is_similar(monster5e["name"], monster["name"]):
            monster5e["environments"] = monster["environments"]
            break

# write the monsters to a json file
date = datetime.datetime.now().strftime("%m-%d-%Y")
folder = f'exports/{date}'

try:
    with open(f'{folder}/monsters.json', 'w') as f:
        json.dump(monsters5e, f, indent=4)
except FileNotFoundError:
    os.mkdir(folder)
    with open(f'{folder}/monsters.json', 'w') as f:
        json.dump(monsters5e, f, indent=4)
