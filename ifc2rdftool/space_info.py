import ifcopenshell.util.element
from rdflib import URIRef
from rdflib.namespace import RDF

from ifc2rdftool.graph_resources import BOT_NAMESPACE, INSTANCE_NAMESPACE
from ifc2rdftool.wall_info import get_element_properties


def add_space_info_to_graph(space_element, graph_model):
    graph_model.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{space_element.GlobalId}"),
            RDF.type,
            BOT_NAMESPACE.Space,
        )
    )
    container = ifcopenshell.util.element.get_container(space_element)
    if container:
        graph_model.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{container.GlobalId}"),
                BOT_NAMESPACE.containsElement,
                URIRef(f"{INSTANCE_NAMESPACE}{space_element.GlobalId}"),
            )
        )
    decomposition = ifcopenshell.util.element.get_decomposition(space_element)
    if decomposition:
        for element in decomposition:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{space_element.GlobalId}"),
                    BOT_NAMESPACE.containsElement,
                    URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                )
            )
    get_element_properties(space_element, graph_model)
