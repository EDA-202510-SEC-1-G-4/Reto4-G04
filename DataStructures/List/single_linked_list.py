def new_list():
    new_list = {
        'first': None,
        'last': None,
        'size': 0
    }
    return new_list

def default_sort_criteria (elm1,elm2):
    is_sorted = False
    if elm1 <= elm2:
      is_sorted = True
    return is_sorted

def get_element (my_list, pos):
    searchpos = 0
    node = my_list['first']
    while searchpos < pos:
        node = node['next']
        searchpos += 1
    return node["info"]

def is_present (my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else:
            temp = temp["next"]
            count += 1
        
    if not is_in_array:
            count = -1
    return count

def add_first (my_list, element):
    new_node = {
        'info': element,
        'next': my_list['first']
    }
    my_list['first'] = new_node
    if my_list['size'] == 0:
        my_list["last"] = new_node
        my_list["first"] = new_node
    my_list['size'] += 1
    return my_list

def add_last (my_list, element):
    new_node = {
        'info': element,
        'next': None
    }
    if my_list['size'] == 0:
        my_list['first'] = new_node
    else:
        my_list['last']['next'] = new_node
    my_list['last'] = new_node
    my_list['size'] += 1
    return my_list

def size(my_list):
    return my_list["size"]

def first_element (my_list):
    return my_list["first"]["info"]

def is_empty (my_list):
    return my_list["size"] == 0

def get_last_element (my_list):
    return my_list["last"]["info"]

def remove_first (my_list):
    my_list["first"]["next"] = None
    my_list ["first"] = my_list["first"]["next"]
    return my_list

def remove_first(my_list):

    if my_list["size"] > 0:
        removed = my_list["first"]["info"]
        my_list["first"] = my_list["first"]["next"]
        my_list["size"] -= 1
        if my_list["size"] == 0:
            my_list["last"] = None
            my_list["first"] = None
        return removed
    return None

def last_element(my_list):
    if my_list["size"] == 0:
        return None
    else:
        return my_list["last"]["info"]
    
def remove_last(my_list):
    if my_list["size"] == 0:
        return None
    elif my_list["size"] == 1:
        return remove_first(my_list)
    else:
        removed = my_list["last"]["info"]
        i = 0
        actual = my_list["first"]
        while i < my_list["size"]:
            actual = actual["next"]
            i += 1
    
        actual["next"] = None
        my_list["last"] = actual
        my_list["size"] -= 1

        if my_list["size"] == 0:
            my_list["last"] = None
            my_list["first"] = None
        return removed

def insert_element(my_list, elm, pos):

    if pos < 0 or pos > my_list["size"]:
        return my_list 
    new_node = {"info": elm, "next": None}

    if pos == 0:
        new_node["next"] = my_list["first"]
        my_list["first"] = new_node
        if my_list["last"] is None:
            my_list["last"] = new_node
    elif pos == my_list["size"]:
        if my_list["last"] is not None:
            my_list["last"]["next"] = new_node
        my_list["last"] = new_node
        if my_list["first"] is None:
            my_list["first"] = new_node
    else:
        prev = my_list["first"]
        for _ in range(pos - 1):
            prev = prev["next"]
        new_node["next"] = prev["next"]
        prev["next"] = new_node

    my_list["size"] += 1
    return my_list


def delete_element(my_list, pos):

    if pos == 0:
        remove_first(my_list) # remove_first already modifies my_list
        return my_list # Return the modified list here
    elif 0 < pos < my_list["size"]:
        prev = my_list["first"]
        for _ in range(pos - 1):
            prev = prev["next"]
        prev["next"] = prev["next"]["next"]
        if prev["next"] is None:
            my_list["last"] = prev
        my_list["size"] -= 1
        return my_list
    return None

def change_info(my_list, pos, new_info):

    if 0 <= pos < my_list["size"]:
        current = my_list["first"]
        for _ in range(pos):
            current = current["next"]
        current["info"] = new_info
        return new_info
    return None

def exchange(my_list, pos1, pos2):

    if 0 <= pos1 < my_list["size"] and 0 <= pos2 < my_list["size"]:
        current1 = my_list["first"]
        for _ in range(pos1):
            current1 = current1["next"]
        current2 = my_list["first"]
        for _ in range(pos2):
            current2 = current2["next"]
        current1["info"], current2["info"] = current2["info"], current1["info"]
        return my_list
    return None

def sub_list(my_list, start, length):

    if not (0 <= start < my_list["size"]) or length <= 0:
        return new_list()

    current = my_list["first"]
    for _ in range(start):
        current = current["next"]

    sublist = new_list()
    for _ in range(length):
        if current is None:
            break
        add_last(sublist, current["info"])
        current = current["next"]
    return sublist

def default_sort_criteria (elm1,elm2):
    is_sorted = False
    if elm1 <= elm2:
      is_sorted = True
    return is_sorted

def default_cmp_function(a, b):
   #n.castano hizo esta calidad pa single"
    return a - b  


def selection_sort(my_list, cmp_function):
    if my_list["size"] < 2:
        return my_list  # No es necesario ordenar si hay 0 o 1 elementos

    current = my_list["first"]
    
    while current is not None:
        min_node = current
        search = current["next"]

        while search is not None:
            if cmp_function(search["info"], min_node["info"]) < 0:
                min_node = search
            search = search["next"]
        
        # Intercambiar valores en lugar de nodos
        if min_node != current:
            current["info"], min_node["info"] = min_node["info"], current["info"]

        current = current["next"]
    
    return my_list    
        
def insertion_sort():
    
    return 0

def shell_sort(list,default_sort_criteria):
    node = list["first"]
    for node in list:
        print(node["info"])
        next = node["next"]
        node = next

        
    return 0
 
def merge_sort():
    return 0

def quick_sort():
    return 0