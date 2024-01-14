import ifcopenshell.util.element
from rdflib import RDF, XSD, Literal, URIRef

from ifc2rdftool.graph_resources import (BEO_NAMESPACE, BOT_NAMESPACE,
                                         CORE_NAMESPACE, DICM_NAMESPACE,
                                         INSTANCE_NAMESPACE)
from ifc2rdftool.wall_info import (get_element_properties,
                                   get_material_triples, get_multiple_guids,
                                   get_valid_guid)


def get_element_material_constituent_info(element, graph_model):
    constituent_set_guid = get_valid_guid()
    constituent_set = ifcopenshell.util.element.get_material(element)
    if constituent_set:
        graph_model.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                DICM_NAMESPACE.hasConstituentSet,
                URIRef(f"{INSTANCE_NAMESPACE}{constituent_set_guid}"),
            )
        )
        graph_model.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{constituent_set_guid}"),
                RDF.type,
                DICM_NAMESPACE.ConstituentSet,
            )
        )
        if constituent_set.get_info()["Name"]:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{constituent_set_guid}"),
                    CORE_NAMESPACE.hasName,
                    Literal(constituent_set.get_info()["Name"]),
                )
            )
        if constituent_set.MaterialConstituents:
            material_constituents = constituent_set.MaterialConstituents
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{constituent_set_guid}"),
                    DICM_NAMESPACE.NumberOfLayers,
                    Literal(len(material_constituents), datatype=XSD.integer),
                )
            )
            material_constituents_guid = get_multiple_guids(len(material_constituents))
            for i in range(len(material_constituents)):
                constituent_guid = material_constituents_guid[i]
                graph_model.add(
                    (
                        URIRef(f"{INSTANCE_NAMESPACE}{constituent_set_guid}"),
                        DICM_NAMESPACE.hasConstituent,
                        URIRef(f"{INSTANCE_NAMESPACE}{constituent_guid}"),
                    )
                )
                graph_model.add(
                    (
                        URIRef(f"{INSTANCE_NAMESPACE}{constituent_guid}"),
                        RDF.type,
                        DICM_NAMESPACE.Constituent,
                    )
                )
                if material_constituents[i].Name:
                    graph_model.add(
                        (
                            URIRef(f"{INSTANCE_NAMESPACE}{constituent_guid}"),
                            CORE_NAMESPACE.hasLabel,
                            Literal(material_constituents[i].get_info()["Name"]),
                        )
                    )
                constituents_property_set = material_constituents[i].get_info()
                for property_name, property_value in constituents_property_set.items():
                    if property_name == "Material":
                        get_material_triples(
                            constituent_guid, property_value, graph_model
                        )


def add_windows_info_to_graph(window_element, graph_model):
    graph_model.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{window_element.GlobalId}"),
            RDF.type,
            BEO_NAMESPACE.Window,
        )
    )
    container = ifcopenshell.util.element.get_container(window_element)
    if container:
        graph_model.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{container.GlobalId}"),
                BOT_NAMESPACE.containsElement,
                URIRef(f"{INSTANCE_NAMESPACE}{window_element.GlobalId}"),
            )
        )
    decomposition = ifcopenshell.util.element.get_decomposition(window_element)
    if decomposition:
        for element in decomposition:
            graph_model.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{window_element.GlobalId}"),
                    BOT_NAMESPACE.containsElement,
                    URIRef(f"{INSTANCE_NAMESPACE}{element.GlobalId}"),
                )
            )
    get_element_properties(window_element, graph_model)
    get_element_material_constituent_info(window_element, graph_model)
