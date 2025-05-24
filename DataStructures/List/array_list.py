import random as rd

def new_list():
    newlist = {
        "elements": [],
        "size": 0
    
    }
    return newlist

def add_first(list, element):
    list['elements'].insert(0, element)
    list['size'] += 1
    return list

def add_last(list, element):
    list['elements'].append(element)
    list['size'] += 1
    return list

def remove_first(list):
    if list['size'] > 0:
        elemento = list['elements'].pop(0)
        list['size'] -= 1
        return elemento
    else: 
        raise Exception('IndexError: list index out of range')
    
def remove_last(list):
    if list['size'] > 0:
        elemento = list['elements'].pop(list['size']-1)
        list['size'] -= 1
        return elemento
    else:
        raise Exception('IndexError: list index out of range')

def insert_element(list, element, pos):
    list['elements'].insert(pos, element)
    list['size'] += 1
    return list

def delete_element(list, index):
    if size(list) > 0 and index >= 0 and index < size(list):
        list['elements'].pop(index)
        list['size'] -= 1
    return list

def size(list):
    return list['size']

def first_element(list):
    if list['size'] != 0:
        return list['elements'][0]

def get_element(list, index):
    return list['elements'][index]    
    
def is_empty(list):
    return list['size'] == 0

def compare_function(element1, element2):
    if element1 == element2:
        return 0
    elif element1 > element2:
        return 1
    else:
        return -1
    
def is_present(my_list, element, compare_function):
    
    size = my_list['size']
    print(f"DEBUG: Checking element={element} with compare_function={compare_function}")
    if size > 0:
        keyexists = False
        for keypos in range (0, size):
            info = my_list['elements'][keypos]
            if compare_function(element, info) == 0:
                keyexists = True
                break
        if keyexists:
            return keypos
    return -1
    
def change_info(list,pos,new_info):
    if pos < list['size']:
        list['elements'].pop(pos)
        list['elements'].insert(pos, new_info)
        return list
    else: 
        raise Exception('IndexError: list index out of range')
    
def exchange(list,pos1,pos2):
    if list['size'] != 0 and pos1 < list['size'] and pos2 < list['size']:
        elem1 = list['elements'][pos1]
        elem2 = list['elements'][pos2] 
        list['elements'].pop(pos1)
        list['elements'].pop(pos2-1)
        list['elements'].insert(pos1,elem2)
        list['elements'].insert(pos2,elem1)
        return list
    else:
        raise Exception('IndexError: list index out of range')
    
def sub_list(list,pos_i,num_elements):
    if pos_i < list['size'] and (num_elements+pos_i) <= list['size']:
        sublist = {
            'size': num_elements,
            'elements':list['elements'][pos_i:pos_i+num_elements]
        }
        return sublist
    else:
        raise Exception('IndexError: list index out of range')
        

def default_sort_criteria (elm1,elm2):
    is_sorted = False
    if elm1 <= elm2:
      is_sorted = True
    return is_sorted
    

def selection_sort(my_list, default_sort_criteria):
    n = size(my_list)
    for i in range(n):
        for min_pos in range(i+1,n):
            if not default_sort_criteria(my_list['elements'][i],my_list['elements'][min_pos]):
                
                exchange(my_list,i,min_pos)
    return my_list         
        
        

def insertion_sort(lista, default_sort_criteria):
    for i in range(1,lista['size']):
        valor = lista['elements'][i]
        j = i-1
        
        while j >= 0 and default_sort_criteria(valor,lista['elements'][j]):
            lista['elements'][j], lista['elements'][j+1] = lista['elements'][j+1], lista['elements'][j]
            j-=1
        lista['elements'][j+1] = valor
    return lista

def shell_sort(list,default_sort_criteria):
    #print(list["elements"])
    h = 1
    while h < size(list):
        h = (3*h) +1
    h //= 3
    h-=1
    while h >= 1:
        i = 0
        for i in range(size(list)-h):
            elm2 = list["elements"][i+h]
            elm1 = list["elements"][i]
            ordenado = False
            if not default_sort_criteria(elm1,elm2):
                exchange(list,i,i+h)
                #print(list["elements"])
                ordenado = False
                j=i
                while not ordenado and j<size(list):
                    if j-h >= 0:
                        new2 = list["elements"][j]
                        new1 = list["elements"][j-h]
                        if not default_sort_criteria(new1,new2): #new1>new2
                            exchange(list,j-h,j)
                            #print(list["elements"])
                            j-=h
                        else: ordenado=True
                    else:j = size(list)
            else:
                ordenado = True   
        h //= 3


    #if h==1:
    # list=selection_sort(list,default_sort_criteria) 
    # NO funciona selection correctamente, por ahora no se puede usar cuando h=1  
    return list
 
def merge_sort(my_list, cmp_function):
    if my_list['size'] <= 1:
        return my_list  # Si la lista tiene 0 o 1 elementos, ya está ordenada.


    mitad = my_list['size'] // 2
    lista1 = {'elements': my_list['elements'][0:mitad], 'size': mitad}
    lista2 = {'elements': my_list['elements'][mitad:], 'size': my_list['size'] - mitad}


    # Llamar a merge_sort recursivamente con la función de comparación
    lista1 = merge_sort(lista1, cmp_function)
    lista2 = merge_sort(lista2, cmp_function)


    return merge_sorted_arrays(lista1, lista2, cmp_function)


def merge_sorted_arrays(lista1, lista2, cmp_function):
    resultado = {'elements': [], 'size': lista1['size'] + lista2['size']}
    i, j = 0, 0


    while i < lista1['size'] and j < lista2['size']:
        if cmp_function(lista1['elements'][i], lista2['elements'][j]) == True:
            resultado['elements'].append(lista1['elements'][i])
            i += 1
        else:
            resultado['elements'].append(lista2['elements'][j])
            j += 1


    while i < lista1['size']:
        resultado['elements'].append(lista1['elements'][i])
        i += 1


    while j < lista2['size']:
        resultado['elements'].append(lista2['elements'][j])
        j += 1


    return resultado

def quick_sort(list,default_sort_criteria,lo,hi):
    
    pivote = partition(list,default_sort_criteria,lo,hi)
    if hi-lo==1 or hi-lo==0 or hi-lo==2: #Esto no siemore es 1
        return list["elements"]
    else:
        rd.shuffle(list["elements"])
        # tengo que mezclar estas dos listas
        return quick_sort(list,default_sort_criteria,lo,pivote-1),quick_sort(list,default_sort_criteria,pivote+1,hi)


def partition (list,default_sort_criteria,lo,hi):
    pivote = hi
    elm_pivote = list["elements"][pivote]
    i = lo
    peque = -1
    while i < hi:
        elm = list["elements"][i]
        if default_sort_criteria(elm,elm_pivote):
            peque = i
            if peque != i:
                exchange(list,peque+1,i)
                print(list["elements"])
        
        i +=1 
    exchange(list,peque+1,pivote)
    print(list["elements"])
    pivote = peque+1
    return pivote
    
 