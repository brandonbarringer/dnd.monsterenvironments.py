"""
Resources:
https://api.open5e.com/monsters/?format=json
https://www.dndbeyond.com/monsters
"""

import json
import difflib
import re
import datetime
from pprint import pprint

with open('data/open5e/monsters.json') as f:
    monsters = json.load(f)

with open('data/kobold_press/monsters_by_terrain.json') as f:
    monsters_environment = json.load(f)

# load the alternate_environment.json file
with open('data/xios_guide_to_monsters/xios_guide_to_monsters.json') as f:
    alt_environment = json.load(f)

environments = ['arctic', 'coastal', 'desert', 'forest', 'grassland', 'hill', 'jungle', 'plain', 'mountain', 'swamp', 'underdark', 'underwater', 'urban', 'badlands', 'any']

word_map = {
    'flame': ['desert', 'badlands', 'mountain', 'plain', 'hill'],
    'stone': ['desert', 'badlands', 'mountain', 'plain', 'underdark', 'urban'],
    'vine': ['forest', 'swamp', 'grassland', 'jungle'],
    'fire': ['desert', 'badlands', 'mountain', 'plain', 'hill'],
    'ice': ['arctic', 'coastal', 'desert', 'badlands', 'mountain', 'plain', 'hill', 'swamp', 'underdark', 'underwater', 'urban', 'void', 'cave', 'sea'],
    'kelp': ['coastal', 'jungle', 'swamp', 'underdark', 'underwater',],
    'sand': ['coastal', 'desert', 'hill', 'plain', 'mountain', 'underdark', 'underwater', 'badlands'],
    'snow': ['arctic', 'coastal', 'mountain', 'urban', 'badlands'],
    'deep': ['hill', 'mountain', 'swamp', 'underdark', 'underwater', 'badlands'],
    'water': ['arctic', 'coastal', 'forest', 'grassland', 'jungle', 'mountain', 'swamp', 'underdark', 'underwater', 'urban'],
    'wind': ['arctic', 'coastal', 'desert', 'grassland', 'hill', 'plain', 'mountain', 'urban', 'badlands'],
    'windy': ['arctic', 'coastal', 'desert', 'grassland', 'hill', 'plain', 'mountain', 'urban', 'badlands'],
    'wood': ['coastal', 'forest', 'grassland', 'hill', 'jungle', 'plain', 'mountain', 'swamp', 'badlands'],
    'imperial': ['arctic', 'coastal', 'forest','jungle','mountain', 'swamp', 'underdark', 'underwater'],
    'wasteland': ['arctic', 'desert', 'grassland', 'hill', 'plain', 'mountain', 'underdark', 'badlands'],
    'boreal': ['arctic', 'coastal', 'plain', 'mountain', 'badlands']
}


def is_name_match(name1:str, name2:str):
    # remove non-alphanumeric characters, keeping spaces
    name1 = re.sub(r'[^a-zA-Z0-9 ]', '', name1)
    name2 = re.sub(r'[^a-zA-Z0-9 ]', '', name2)

    name1 = name1.lower()
    name2 = name2.lower()
    # if the names are the same, return true
    if name1 == name2:
        return True

    n1 = name1.split(' ')
    n2 = name2.split(' ')

    # if none of the words in the name are in the other name, return false
    if not any(word in n2 for word in n1) and not any(word in n1 for word in n2):
        return False

    # if each word in the name is in the other name, return true
    if (all(word in n2 for word in n1) or all(word in n1 for word in n2)) and len(n1) == len(n2):
        return True

    colors = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'silver', 'white', 'yellow', 'crimson', 'golden', 'ivory', 'jet', 'ochre', 'olive', 'scarlet', 'tan', 'violet', 'azure', 'cerulean', 'indigo', 'magenta', 'mauve', 'teal', 'turquoise', 'vermilion', 'viridian']
    metals = ['brass', 'bronze', 'copper', 'gold', 'iron', 'lead', 'platinum', 'silver', 'steel', 'tin', 'mithral', 'adamantine', 'mercury', 'orium', 'cobalt']
    environs = ['arctic', 'coastal', 'desert', 'forest', 'grassland', 'hill', 'mountain', 'swamp', 'underdark', 'underwater', 'urban', 'void', 'cave', 'sea']
    types = ['flame', 'light', 'dark', 'shadow', 'stone', 'vine', 'fire', 'ice', 'kelp', 'sand', 'snow', 'deep', 'water', 'wind', 'windy', 'wood', 'imperial', 'wasteland', 'boreal']
    differentiators = [*colors, *metals, *environs, *types]

    # if all of the words are the same, except for differentiators, return false
    if all(word in differentiators for word in n1) and all(word in differentiators for word in n2):
        return False

    return False

# remove duplicates
for key in monsters_environment:
    monsters_environment[key] = list(dict.fromkeys(monsters_environment[key]))

# remove empty values
for i in range(len(alt_environment)):
    alt_environment[i] = { k: v for k, v in alt_environment[i].items() if v != '' }
    # if the environment key exists
    if 'Environment' in alt_environment[i]:
        # transform the environment key into a list and trim whitespace
        alt_environment[i]['Environment'] = [x.strip() for x in alt_environment[i]['Environment'].split(',')]

# merge objects with the same name
alt_merged = []
names = set()
for i in range(len(alt_environment)):
    name = alt_environment[i]["Name"]
    if name in names:
        for merged in alt_merged:
            if merged["Name"] == name:
                merged.update(alt_environment[i])
                break
    else:
        names.add(name)
        alt_merged.append(alt_environment[i])

for monster in monsters:
    monster['environment'] = []

for alt_monster in alt_merged:
    for monster in monsters:
        if is_name_match(monster['name'], alt_monster['Name']):
            if 'Environment' in alt_monster:
                monster['environment'] = alt_monster['Environment']
                break

# for each key in the monsters_environment dictionary
for key in monsters_environment:
    # for each monster in the monsters list
    for monster_env in monsters_environment[key]:
        # for each monster in the monsters list
        for monster in monsters:
            # if the monster name is similar to the monster in the monsters_environment dictionary
            if is_name_match(monster['name'], monster_env):
                # add the environment to the monster
                monster['environment'].append(key) if key not in monster['environment'] else None
                break

# monsters with environment
monsters_with_env = [monster for monster in monsters if len(monster['environment']) > 0]

# write the monsters to a json file
date = datetime.datetime.now().strftime("%Y-%m-%d")
with open(f'monsters-{date}.json', 'w') as f:
    json.dump(monsters_with_env, f, indent=4)
