import ifcopenshell.util.element
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from ifc2rdftool.graph_resources import BOT_NAMESPACE, INSTANCE_NAMESPACE


def add_storey_info_to_graph(storey_entity, graph: Graph):
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{storey_entity.GlobalId}"),
            RDF.type,
            BOT_NAMESPACE.Storey,
        )
    )
    decomposition = ifcopenshell.util.element.get_aggregate(storey_entity)
    if decomposition:
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{decomposition.GlobalId}"),
                BOT_NAMESPACE.hasStorey,
                URIRef(f"{INSTANCE_NAMESPACE}{storey_entity.GlobalId}"),
            )
        )
