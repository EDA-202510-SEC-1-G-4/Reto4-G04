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
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail

def rehash(my_map):
    capacity = int(my_map['capacity'])
    num = mp.next_prime(capacity*2)
    resized = new_map(num,factores=0.5,primo=1093598347)
    elements = my_map['table']['elements']
    for element in elements:
        if element['key'] != None and element['value'] != None:
            llave = element['key']
            valor = element['value']
            put(resized,llave,valor)
    return resized

def put(my_map,key,value):
    pos = int(mp.hash_value(my_map,key)%my_map['table']['size'])
    pos_key = my_map['table']['elements'][pos]['key']
    if pos_key == None or pos_key == "__EMPTY__":
        al.change_info(my_map['table'],pos,{'key':key,'value':value})
        my_map['size'] += 1
        my_map['current_factor'] = round(my_map['size'] / my_map['table']['size'], 2)
    elif pos_key == key:
        al.change_info(my_map['table'],pos,{'key':key,'value':value})
        my_map['current_factor'] = round(my_map['size'] / my_map['table']['size'], 2)
    else:
        if pos <= al.size(my_map["table"]):
            boolx, pos = find_slot(my_map,key,mp.hash_value(my_map,key))
            
            pos_key = my_map['table']["elements"][pos]['key']
            if pos_key == key:
                al.change_info(my_map['table'],pos,{'key':key,'value':value})
                my_map['current_factor'] = round(my_map['size'] / my_map['table']['size'], 2)
            elif not boolx:
                al.change_info(my_map['table'],pos,{'key':key,'value':value})
    if my_map['current_factor'] >= my_map['limit_factor']:
        my_map = rehash(my_map)
    return my_map

def contains(map, key):
    cont = False
    if map['table']['size'] > 0:
        for pair in map['table']['elements']:
            k = pair['key']
            if k == key:
                cont = True
    return cont

def get(map, key):
    res = None
    if contains(map,key):
        hash = mp.hash_value(map,key)
        if hash <= al.size(map["table"]):
            if map['table']['elements'][hash]['key'] == key:
                res = map['table']['elements'][hash]['value'] 
            else:
                cent = True
                while cent: 
                    res = map['table']['elements'][hash]['value']
                    if map['table']['elements'][hash]['key'] == key:
                        cent = False
                hash += 1
    return res

def remove(map,key): 
    slot = mp.hash_value(map,key)%map['table']['size']
    if map['table']['elements'][slot]['key'] == key:
        map['table']['elements'][slot]['key'] = "__EMPTY__"
        map['table']['elements'][slot]['value'] = None
        map['size'] -= 1
    else:
        boolx, pos = find_slot(map,key,mp.hash_value(map,key))
        if boolx:
            map['table']['elements'][pos]['key'] = "__EMPTY__"
            map['table']['elements'][pos]['value'] = None
            map['size'] -= 1
    return map

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