def new_dijsktra_search(source):
    """

    Crea una estructura de busqueda usada en el algoritmo **dijsktra**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **source**: Vertice de origen. Se inicializa en ``source``
    - **visited**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **pq**: Cola indexada con los vertices visitados. Se inicializa en ``None``

    :returns: Estructura de busqueda
    :rtype: dijsktra_search
    """
    search = {"source": source, "visited": None, "pq": None}
