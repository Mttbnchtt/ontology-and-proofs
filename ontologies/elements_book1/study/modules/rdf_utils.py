import rdflib

def read_graph(file_path: str, format: str = "turtle") -> rdflib.Graph:
    """
    Reads an RDF graph from a file.
    """
    g = rdflib.Graph()
    g.parse(file_path, format=format)
    print(f"Graph has {len(g)} statements.")
    return g