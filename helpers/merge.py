def to_set(value):
    if isinstance(value, list):
        return set(value)
    elif isinstance(value, str):
        return {value}
    return value

def merge_monster(monster1: dict, monster2: dict) -> dict:

    # we only care about merging the environments
    if 'environments' in monster1 and 'environments' in monster2:
        # merge the environments by converting them to sets
        monster1['environments'] = to_set(monster1['environments'])
        monster2['environments'] = to_set(monster2['environments'])
        monster1['environments'] = monster1['environments'].union(monster2['environments'])

        # convert the environments back to a list
        monster1['environments'] = list(monster1['environments'])

    return monster1

