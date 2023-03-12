import json

with open('exports/03-11-2023/monsters.json') as f:
    monsters = json.load(f)

# monsters with environment
monsters_with_env = [monster for monster in monsters if 'environments' in monster]

print(len(monsters_with_env))
print(len(monsters))
