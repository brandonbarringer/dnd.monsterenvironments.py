import json
import datetime
from pprint import pprint

with open('../exports/monsters-2023-03-05.json') as f:
    monsters = json.load(f)

environments = ['arctic', 'coastal', 'desert', 'forest', 'grassland', 'hill', 'jungle', 'plain', 'mountain', 'swamp', 'underdark', 'underwater', 'urban', 'badlands', 'any']

crs = ['0', '1/8', '1/4', '1/2', *[str(i) for i in range(1, 31)]]

for env in environments:
    for cr in crs:
        data = {
            'count': 0,
            'monsters': []
        }
        for monster in monsters:
            if monster['challenge_rating'] == cr and env in monster['environment']:
                data['monsters'].append(monster)
                data['count'] += 1
        if data['count'] > 0:
            cr_str = cr.replace('/', '-')
            with open(f'03-05-2023/{env}/{cr_str}.json', 'w') as f:
                json.dump(data, f, indent=4)
