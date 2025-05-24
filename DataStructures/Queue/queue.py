from DataStructures.List import array_list as arreglo

def new_queue ():
    queue = arreglo.new_list()
    return queue

def enqueue (queue, element):
    queue = arreglo.add_last(queue, element)
    return queue

def dequeue (queue):
    if arreglo.size(queue) > 0:
        queue = arreglo.remove_first(queue)
    elif arreglo.size(queue) == 0:
        raise Exception('EmptyStructureError: queue is empty')
    return queue

def peek (queue):
    if arreglo.size(queue) > 0:
        first = arreglo.first_element(queue)
    elif arreglo.size(queue) == 0:
        raise Exception('EmptyStructureError: queue is empty')
    return first

def size(queue):
    return arreglo.size(queue)

def is_empty(queue):
    return arreglo.size(queue) == 0 



