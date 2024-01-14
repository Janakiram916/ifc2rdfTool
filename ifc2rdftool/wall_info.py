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


def create_property_triple(property_type, value, element, graph):
    property_guid = get_valid_guid()
    property_uri = URIRef(f"{INSTANCE_NAMESPACE}{property_guid}")
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{element}"),
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


def get_material_triples(element, material, graph_model):
    material_guid = get_valid_guid()
    material_uri = URIRef(f"{INSTANCE_NAMESPACE}{material_guid}")
    graph_model.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{element}"),
            DICM_NAMESPACE.hasMaterial,
            material_uri,
        )
    )
    graph_model.add(
        (
            material_uri,
            RDF.type,
            DICM_NAMESPACE.Material,
        )
    )
    graph_model.add(
        (
            material_uri,
            CORE_NAMESPACE.hasLabel,
            Literal(material.get_info()["Name"]),
        )
    )


def get_element_layer_info(element, graph_model):
    layer_set_guid = get_valid_guid()
    layer_set_usage = ifcopenshell.util.element.get_material(element)
    if layer_set_usage:
        layer_set = layer_set_usage
        if layer_set_usage.get_info()["type"] == "IfcMaterialLayerSetUsage":
            layer_set = layer_set_usage.ForLayerSet
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
            if layer_set.get_info()["LayerSetName"]:
                graph_model.add(
                    (
                        URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                        CORE_NAMESPACE.hasName,
                        Literal(layer_set.get_info()["LayerSetName"]),
                    )
                )
            if layer_set.MaterialLayers:
                layers = layer_set.MaterialLayers
                graph_model.add(
                    (
                        URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                        DICM_NAMESPACE.NumberOfLayers,
                        Literal(len(layers), datatype=XSD.integer),
                    )
                )
                layers_guid = get_multiple_guids(len(layers))
                for i in range(len(layers)):
                    layer_guid = layers_guid[i]
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{layer_set_guid}"),
                            DICM_NAMESPACE.hasLayer,
                            URIRef(f"{INSTANCE_NAMESPACE}{layer_guid}"),
                        )
                    )
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{layer_guid}"),
                            RDF.type,
                            DICM_NAMESPACE.Layer,
                        )
                    )
                    if layers[i].Name:
                        graph_model.add(
                            (
                                URIRef(f"{INSTANCE_NAMESPACE}{layer_guid}"),
                                CORE_NAMESPACE.hasLabel,
                                Literal(layers[i].get_info()["Name"]),
                            )
                        )
                    layer_property_set = layers[i].get_info()
                    for property_name, property_value in layer_property_set.items():
                        if property_name == "LayerThickness":
                            create_property_triple(
                                property_name,
                                property_value,
                                layer_guid,
                                graph_model,
                            )
                        if property_name == "Material":
                            get_material_triples(
                                layer_guid, property_value, graph_model
                            )


def get_element_properties(element, rdf_graph):
    psets_and_qtos = ifcopenshell.util.element.get_psets(element)
    element_guid = element.GlobalId
    for property_set_key, property_key in psets_and_qtos.items():
        if property_set_key in [
            "Pset_WallCommon",
            "Pset_SlabCommon",
            "Pset_SpaceCommon",
            "Pset_WindowCommon",
            "Pset_DoorCommon",
        ]:
            for property_name, property_value in property_key.items():
                if property_name == "ThermalTransmittance":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "IsExternal":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
        if property_set_key in [
            "Qto_WallBaseQuantities",
            "Qto_SlabBaseQuantities",
            "Qto_SpaceBaseQuantities",
            "Qto_WindowBaseQuantities",
            "Qto_DoorBaseQuantities",
        ]:
            for property_name, property_value in property_key.items():
                if property_name == "Length":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "Height":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "Width":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "GrossArea":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "GrossVolume":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "NetArea":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "NetVolume":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "Perimeter":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "NetFloorArea":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "Area":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
        if property_set_key == "Analytical Properties":
            for property_name, property_value in property_key.items():
                if property_name == "Absorptance":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "Roughness":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "Thermal Resistance (R)":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
                    )
                if property_name == "Thermal Mass":
                    create_property_triple(
                        property_name, property_value, element_guid, rdf_graph
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
    get_element_properties(wall_element, graph_model)
