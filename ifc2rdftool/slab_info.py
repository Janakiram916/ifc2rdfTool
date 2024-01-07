import ifcopenshell.util.element
from rdflib import URIRef
from rdflib.namespace import RDF

from ifc2rdftool.graph_resources import (BEO_NAMESPACE, BOT_NAMESPACE,
                                         INSTANCE_NAMESPACE)
from ifc2rdftool.wall_info import get_element_layer_info

# def get_slab_properties(slab_element, rdf_graph):
# psets_and_qtos = ifcopenshell.util.element.get_psets(slab_element)
# ic(psets_and_qtos)
# wall_element_guid = slab_element.GlobalId
# for property_set_key, property_key in psets_and_qtos.items():
#     if property_set_key == "Pset_WallCommon":
#         for property_name, property_value in property_key.items():
#             if property_name == "ThermalTransmittance":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#             elif property_name == "IsExternal":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#     elif property_set_key == "Qto_WallBaseQuantities":
#         for property_name, property_value in property_key.items():
#             if property_name == "Length":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#             elif property_name == "Height":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#             elif property_name == "Width":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#     elif property_set_key == "Analytical Properties":
#         for property_name, property_value in property_key.items():
#             if property_name == "Absorptance":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#             elif property_name == "Roughness":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#             elif property_name == "Thermal Resistance (R)":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )
#             elif property_name == "Thermal Mass":
#                 create_property_triple(
#                     property_name, property_value, wall_element_guid, rdf_graph
#                 )


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
