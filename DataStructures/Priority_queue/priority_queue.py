from DataStructures.List import array_list as al
from DataStructures.Priority_queue import index_pq_entry as pqe
from DataStructures.List import array_list as al

def new_heap(is_min_pq=True):
    heap = {'elements':al.new_list(),
            'size':0,
            'cmp_function':default_compare_lower_value}
    if is_min_pq == False:
        heap['cmp_function'] = default_compare_higher_value
    return heap

def size(pq):
    return pq["size"]

def is_empty(pq):
    return pq["size"] == 0

def get_first_priority(heap):
    first = None
    if heap['size'] > 0:
        first = heap['elements']['elements'][1]['value']
    return first

def insert(heap,value,key):
    if heap != None:
        elem = {'key':key,
                'value':value}
        al.add_last(heap['elements'],elem)
        pos = al.size(heap['elements'])
        heap["size"]+= 1
        swim(heap,pos)
        
    return heap

def remove(heap):
    if not is_empty(heap):
        retorno = heap["elements"]["elements"][1]["value"]
        heap["elements"]["elements"][1] = heap["elements"]["elements"][heap["size"]-1]
        al.remove_last(heap["elements"])
        
        sink(heap,1)
        heap["size"]=-1
    else:
        retorno = None
    return retorno

def swim(heap,pos):
    if heap['size'] > 0:
        stop = False
        cmp_function = heap['cmp_function']
        while heap["size"]>pos>0 and not stop or pos//2 == 1:
            elem = heap['elements']['elements'][pos]
            padre = heap['elements']['elements'][pos//2]
            if cmp_function(padre,elem):
                heap['elements']['elements'][pos//2] = elem
                heap['elements']['elements'][pos] = padre
                pos = pos//2
            else:
                stop = True
    return heap

def mayor_prioridad(heap,nodo1,nodo2):
    func_comp = heap["cmp_function"]
    if func_comp(nodo1,nodo2):
        return nodo1
    else:
        return nodo2
    
def tiene_hijos(pos,heap):
    if 2*pos < heap["size"] and (2*pos)+1 < heap["size"]:
        return True
    return False
    
def tiene_hijo(pos,heap):
    if 2*pos < heap["size"]:
        return True
    return False

def get_hijos(pos,heap):
    hijo2 = heap["elements"]["elements"][pos]
    hijo1 = heap["elements"]["elements"][pos]
    
    if tiene_hijo(pos,heap):    
        hijo1 = heap["elements"]["elements"][(2*pos)]
        if tiene_hijos(pos,heap):
            hijo2 = heap["elements"]["elements"][(2*pos)+1]
            
    return hijo1,hijo2

def sink(heap,pos):
    if not is_empty(heap):
        func_comp = heap["cmp_function"]
        padre = heap["elements"]["elements"][pos]
        hijo1,hijo2 = get_hijos(pos,heap)
        while func_comp(padre,hijo1) or func_comp(padre,hijo2) and tiene_hijo(pos,heap):
                hijo = mayor_prioridad(heap,hijo1,hijo2)
                if hijo == hijo1:
                    pos *=2
                elif hijo == hijo2:
                    pos = (2*pos) + 1
                    
                temp = padre
                padre = hijo
                hijo = temp
                
                padre = heap["elements"]["elements"][pos]
                hijo1,hijo2=get_hijos(pos,heap)
    
    return heap

def default_compare_higher_value(father_node, child_node):
    if pqe.get_key(father_node) >= pqe.get_key(child_node):
        
        return True
    return False

def default_compare_lower_value(father_node, child_node):
    if pqe.get_key(father_node) <= pqe.get_key(child_node):
        return True
    return False