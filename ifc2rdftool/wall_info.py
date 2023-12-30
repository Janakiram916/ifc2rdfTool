import ifcopenshell.util.element
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD

from ifc2rdftool.graph_resources import (BEO_NAMESPACE, BOT_NAMESPACE,
                                         CORE_NAMESPACE, DICM_NAMESPACE,
                                         DICV_NAMESPACE, INSTANCE_NAMESPACE)


def get_valid_guid() -> str:
    new_id = ifcopenshell.guid.new()
    while "$" in new_id:
        new_id = ifcopenshell.guid.new()
    return new_id


def get_multiple_guids(required_guids: int) -> list:
    guid_list = []
    for _ in range(required_guids):
        guid = get_valid_guid()
        guid_list.append(guid)
    return guid_list


def get_element_layer_info(element, graph_model):
    layer_set_guid = get_valid_guid()
    layer_set_usage = ifcopenshell.util.element.get_material(element).get_info()
    if layer_set_usage:
        layer_set = layer_set_usage["ForLayerSet"]
        if layer_set:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                    DICM_NAMESPACE.hasLayerSet,
                    URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                )
            )
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                    RDF.type,
                    DICM_NAMESPACE.LayerSet,
                )
            )
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                    CORE_NAMESPACE.hasName,
                    Literal(layer_set.get_info()["LayerSetName"]),
                )
            )
            layers = layer_set.MaterialLayers
            if layers:
                graph_model.add(
                    (
                        URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                        DICM_NAMESPACE.NumberOfLayers,
                        Literal(len(layers), datatype=XSD.integer),
                    )
                )
                layers_guid = get_multiple_guids(len(layers))
                for i in range(len(layers)):
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                            DICM_NAMESPACE.hasLayer,
                            URIRef(f"{INSTANCE_NAMESPACE}{layers_guid[i]}"),
                        )
                    )
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{layers_guid[i]}"),
                            RDF.type,
                            DICM_NAMESPACE.Layer,
                        )
                    )
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{layers_guid[i]}"),
                            CORE_NAMESPACE.hasLabel,
                            Literal(layers[i].get_info()["Name"]),
                        )
                    )
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{layers_guid[i]}"),
                            DICM_NAMESPACE.hasThickness,
                            Literal(
                                layers[i].get_info()["LayerThickness"],
                                datatype=XSD.double,
                            ),
                        )
                    )
                    if layers[i].Material:
                        graph_model.add(
                            (
                                URIRef(f"{INSTANCE_NAMESPACE}{layers_guid[i]}"),
                                DICM_NAMESPACE.hasMaterial,
                                Literal(layers[i].Material.get_info()["Name"]),
                            )
                        )


def create_property_triple(property_type, value, element, graph):
    property_guid = get_valid_guid()
    property_uri = URIRef(f"{INSTANCE_NAMESPACE}{property_guid}")
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
            DICV_NAMESPACE.hasProperty,
            property_uri,
        )
    )
    graph.add(
        (
            property_uri,
            RDF.type,
            DICV_NAMESPACE.Property,
        )
    )
    graph.add(
        (
            property_uri,
            CORE_NAMESPACE.hasLabel,
            Literal(property_type),
        )
    )
    graph.add(
        (
            property_uri,
            CORE_NAMESPACE.hasValue,
            Literal(value),
        )
    )


def get_wall_properties(wall_element, rdf_graph):
    psets_and_qtos = ifcopenshell.util.element.get_psets(wall_element)
    for property_set_key, property_key in psets_and_qtos.items():
        if property_set_key == "Pset_WallCommon":
            for property_name, property_value in property_key.items():
                if property_name == "ThermalTransmittance":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
                elif property_name == "IsExternal":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
        elif property_set_key == "Qto_WallBaseQuantities":
            for property_name, property_value in property_key.items():
                if property_name == "Length":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
                elif property_name == "Height":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
                elif property_name == "Width":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
        elif property_set_key == "Analytical Properties":
            for property_name, property_value in property_key.items():
                if property_name == "Absorptance":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
                elif property_name == "Roughness":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
                elif property_name == "Thermal Resistance (R)":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )
                elif property_name == "Thermal Mass":
                    create_property_triple(
                        property_name, property_value, wall_element, rdf_graph
                    )


def add_wall_info_to_graph(wall_element, graph_model):
    graph_model.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{wall_element.GlobalId}"),
            RDF.type,
            BEO_NAMESPACE.Wall,
        )
    )
    container = ifcopenshell.util.element.get_container(wall_element)
    if container:
        graph_model.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{container.GlobalId}"),
                BOT_NAMESPACE.containsElement,
                URIRef(f"{INSTANCE_NAMESPACE}{wall_element.GlobalId}"),
            )
        )
    decomposition = ifcopenshell.util.element.get_decomposition(wall_element)
    if decomposition:
        for element in decomposition:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{wall_element.GlobalId}"),
                    BOT_NAMESPACE.containsElement,
                    URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                )
            )
    get_element_layer_info(wall_element, graph_model)
    get_wall_properties(wall_element, graph_model)
