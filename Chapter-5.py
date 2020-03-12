""" 
Chapter 5: Modules, Packeges, Programs

    dict.setdefault()
        Insert a key with a default value if key is not in dict
        Returns the value of key if key is in dict, else return the default value

        Good when working with dict and not knowing if a key is already present

    defaultdict() (from collections)
        Defaults all vlaues for any key.. Arguments is a function that returns a value and to default to a specific data type (int, string, list, dict). Without this argument, values return are None for all new keys

    counter() (from collections)
    most_common() - orders in descending order
    deque() - stack and queue data type, that allows insert/remove of either end of the structure
        deque.pop()
        deque.popleft()
    
    itertools package library
    chain()
    cycle()
    accumatate()
    pprint() - pretty print


"""
from collections import defaultdict
# Using defaultdic to make a counter

food_counter = defaultdict(int)
# for each occurance of a food-item, create a key of the food-item, assigned the value of occurance to the key until the loop completes
# counter(food_counter) provides the same functionality
for food in ['spam', 'spam', 'eggs', 'spam']:
    food_counter[food] += 1

for food, count in food_counter.items():
    print(food, count)

