import ifcopenshell.util.element
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from ifc2rdftool.graph_resources import BOT_NAMESPACE, INSTANCE_NAMESPACE


def get_relationship_with_spaces(storey, storey_graph: Graph) -> None:
    relationship = storey.IsDecomposedBy
    if relationship:
        space_entities = relationship[0].RelatedObjects
        if space_entities:
            for space_entity in space_entities:
                storey_graph.add(
                    (
                        URIRef(f"{INSTANCE_NAMESPACE}{storey.GlobalId}"),
                        BOT_NAMESPACE.hasSpace,
                        URIRef(f"{INSTANCE_NAMESPACE}{space_entity.GlobalId}"),
                    )
                )


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
    get_relationship_with_spaces(storey_entity, graph)
