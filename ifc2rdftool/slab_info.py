import ifcopenshell.util.element
from rdflib import URIRef
from rdflib.namespace import RDF

from ifc2rdftool.graph_resources import BEO_NAMESPACE, BOT_NAMESPACE, INSTANCE_NAMESPACE
from ifc2rdftool.wall_info import get_element_layer_info, get_element_properties


def add_slab_info_to_graph(slab_element, graph_model):
    graph_model.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{slab_element.GlobalId}"),
            RDF.type,
            BEO_NAMESPACE.Slab,
        )
    )
    container = ifcopenshell.util.element.get_container(slab_element)
    if container:
        graph_model.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{container.GlobalId}"),
                BOT_NAMESPACE.containsElement,
                URIRef(f"{INSTANCE_NAMESPACE}{slab_element.GlobalId}"),
            )
        )
    decomposition = ifcopenshell.util.element.get_decomposition(slab_element)
    if decomposition:
        for element in decomposition:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{slab_element.GlobalId}"),
                    BOT_NAMESPACE.containsElement,
                    URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                )
            )
    get_element_layer_info(slab_element, graph_model)
    get_element_properties(slab_element, graph_model)
