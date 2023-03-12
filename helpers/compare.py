"""
This file contains functions to compare names and other strings.
"""

import re

def name_is_similar(name1, name2):
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
