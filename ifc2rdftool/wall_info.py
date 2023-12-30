import ifcopenshell.util.element
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD

from ifc2rdftool.graph_resources import (BEO_NAMESPACE, BOT_NAMESPACE,
                                         CORE_NAMESPACE, DICM_NAMESPACE,
                                         INSTANCE_NAMESPACE)

LAYER_SET_GUID = ifcopenshell.guid.new()


def get_multiple_guids(number_of_layers):
    return [ifcopenshell.guid.new() for _ in range(number_of_layers)]


def get_element_layer_info(element, graph_model):
    layer_set_usage = ifcopenshell.util.element.get_material(element).get_info()
    if layer_set_usage:
        layer_set = layer_set_usage["ForLayerSet"]
        if layer_set:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                    DICM_NAMESPACE.hasLayerSet,
                    URIRef(f"{INSTANCE_NAMESPACE}{LAYER_SET_GUID}"),
                )
            )
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{LAYER_SET_GUID}"),
                    RDF.type,
                    DICM_NAMESPACE.LayerSet,
                )
            )
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{LAYER_SET_GUID}"),
                    CORE_NAMESPACE.hasName,
                    Literal(layer_set.get_info()["LayerSetName"]),
                )
            )
            layers = layer_set.MaterialLayers
            if layers:
                graph_model.add(
                    (
                        URIRef(f"{INSTANCE_NAMESPACE}{LAYER_SET_GUID}"),
                        DICM_NAMESPACE.NumberOfLayers,
                        Literal(len(layers), datatype=XSD.integer),
                    )
                )
                layers_guid = get_multiple_guids(len(layers))
                for i in range(len(layers)):
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{LAYER_SET_GUID}"),
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
