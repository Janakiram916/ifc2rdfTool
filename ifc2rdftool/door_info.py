import ifcopenshell.util.element
from rdflib import RDF, URIRef

from ifc2rdftool.graph_resources import BEO_NAMESPACE, BOT_NAMESPACE, INSTANCE_NAMESPACE
from ifc2rdftool.wall_info import get_element_properties
from ifc2rdftool.windows_info import get_element_material_constituent_info


def add_door_info_to_graph(door_element, graph_model):
    graph_model.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{door_element.GlobalId}"),
            RDF.type,
            BEO_NAMESPACE.Door,
        )
    )
    container = ifcopenshell.util.element.get_container(door_element)
    if container:
        graph_model.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{container.GlobalId}"),
                BOT_NAMESPACE.containsElement,
                URIRef(f"{INSTANCE_NAMESPACE}{door_element.GlobalId}"),
            )
        )
    decomposition = ifcopenshell.util.element.get_decomposition(door_element)
    if decomposition:
        for element in decomposition:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{door_element.GlobalId}"),
                    BOT_NAMESPACE.containsElement,
                    URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                )
            )
    get_element_properties(door_element, graph_model)
    get_element_material_constituent_info(door_element, graph_model)
