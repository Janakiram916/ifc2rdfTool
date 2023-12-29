import ifcopenshell.util.element
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from ifc2rdftool.graph_resources import BOT_NAMESPACE, INSTANCE_NAMESPACE


def add_building_info_to_graph(building_entity, graph: Graph):
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{building_entity.GlobalId}"),
            RDF.type,
            BOT_NAMESPACE.Building,
        )
    )
    decomposition = ifcopenshell.util.element.get_aggregate(building_entity)
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{decomposition.GlobalId}"),
            BOT_NAMESPACE.hasBuilding,
            URIRef(f"{INSTANCE_NAMESPACE}{building_entity.GlobalId}"),
        )
    )
