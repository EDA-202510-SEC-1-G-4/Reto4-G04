from DataStructures.Map import map_functions as mp
from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me

def new_map(num, factores=0.5, primo=109345121):
    mapa = {}
    mapa["prime"] = primo
    mapa["capacity"] = mp.next_prime(num*2)
    if mapa['capacity'] == 0:
        mapa['capacity'] = mp.next_prime(6) 
    mapa["scale"] = 1
    mapa["shift"] = 0
    mapa["table"] = al.new_list()
    for i in range(mapa['capacity']):
        al.add_last(mapa["table"],{"key": None, "value": None})

    mapa["limit_factor"]= factores
    mapa ["size"] = 0
    mapa["current_factor"] = 0
    return mapa

def default_compare(key, entry):
   if entry is not None and me.get_key(entry) is not None:
        if key == me.get_key(entry):
            return 0
        elif key > me.get_key(entry):
            return 1
        return -1
   else: 
       return -1

def is_available(table, pos):
   if pos <= al.size(table):
        entry = al.get_element(table, pos)
        if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
            return True
   return False

def find_slot(my_map, key, hash_value):
    first_avail = None
    found = False
    ocupied = False
    for _ in range(my_map['capacity']*2):
      if is_available(my_map["table"], hash_value):
            if first_avail == None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               break
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            ocupied = True
            break
      hash_value = (hash_value + 1) % my_map["capacity"]
    
    if first_avail == None:
       ocupied = True
       first_avail = hash_value
    return ocupied, first_avail

def rehash(my_map):
    new_capacity = mp.next_prime(my_map["capacity"] * 2)
    resized_map = new_map(new_capacity, factores=my_map["limit_factor"], primo=1093598347)

    for entry in my_map["table"]["elements"]:
        if entry["key"] is not None and entry["key"] != "__EMPTY__":
            put(resized_map, entry["key"], entry["value"])

    return resized_map

def put(my_map, key, value):
    hash_value = mp.hash_value(my_map, key) % my_map["capacity"]
    ocupied, pos = find_slot(my_map, key, hash_value)

    if ocupied:
        al.change_info(my_map["table"], pos, {'key': key, 'value': value})
    else:
        al.change_info(my_map["table"], pos, {'key': key, 'value': value})
        my_map["size"] += 1
        my_map["current_factor"] = round(my_map["size"] / my_map["capacity"], 2)

        if my_map["current_factor"] >= my_map["limit_factor"]:
            my_map = rehash(my_map)

    return my_map

def contains(my_map, key):
    hash_value = mp.hash_value(my_map, key) % my_map["capacity"]
    ocupied, _ = find_slot(my_map, key, hash_value)
    return ocupied

def get(map, key):
    hash_value = mp.hash_value(map, key)
    found, pos = find_slot(map, key, hash_value)
    if found:
        return al.get_element(map["table"], pos)["value"]
    return None

def remove(my_map, key):
    hash_value = mp.hash_value(my_map, key) % my_map["capacity"]
    ocupied, pos = find_slot(my_map, key, hash_value)

    if ocupied:
        al.change_info(my_map["table"], pos, {'key': "__EMPTY__", 'value': None})
        my_map["size"] -= 1
        my_map["current_factor"] = round(my_map["size"] / my_map["capacity"], 2)

    return my_map

def key_set(map):
    tabla = map['table']['elements']
    keys = al.new_list()
    for pareja in tabla:
        if pareja['key'] != None and pareja['key'] != "__EMPTY__":
            al.add_last(keys,pareja['key'])
    return keys

def value_set(map):
    tabla = map['table']['elements']
    values = al.new_list()
    for pareja in tabla:
        if pareja['value'] != None and pareja['value'] != "__EMPTY__":
            al.add_last(values,pareja['value'])
    return values

def size(map):
   return map["size"]


def is_empty(map):
   return map["size"] == 0