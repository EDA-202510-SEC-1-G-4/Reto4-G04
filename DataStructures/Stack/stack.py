from DataStructures.List import array_list as lt

def new_stack():
    stack = lt.new_list()
    return stack

def push(stack, element):
    lt.add_last(stack, element)
    return stack

def pop(stack):
    dato = None
    if is_empty(stack) == False:
        dato = lt.get_element(stack,lt.size(stack)-1)
        lt.delete_element(stack,lt.size(stack)-1)
    else:
        raise Exception('EmptyStructureError: stack is empty')
    return dato

def size(stack):
    return lt.size(stack)

def is_empty(stack):
    return lt.size(stack) == 0

def top(stack):
    if lt.size(stack) > 0:
        return lt.get_element(stack,lt.size(stack)-1)
    elif lt.size(stack) == 0:
        raise Exception('EmptyStructureError: stack is empty')
