def new_graph_search(source):
    """
    Crea una estructura de busqueda usada en los algoritmos **bfs** y **dfs**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **source**: Vertice de inicio del recorrido. Se usa el vertice ``source``
    - **visited**: Mapa con los vertices visitados. Se inicializa en ``None``

    :param source: Vertice de inicio del recorrido
    :type source: any

    :returns: Estructura de busqueda
    :rtype: graph_search
    """

    search = {"source": source, "visited": None}

    return search
