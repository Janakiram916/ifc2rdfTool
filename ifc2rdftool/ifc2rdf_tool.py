import ifcopenshell
from icecream import ic
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

from ifc2rdftool.graph_resources import (BOT_NAMESPACE, GEO_NAMESPACE,
                                         INSTANCE_NAMESPACE,
                                         LIFECYCLE_NAMESPACE)


def initialize_graph() -> Graph:
    instance_graph = Graph()
    instance_graph.bind("inst", INSTANCE_NAMESPACE)
    instance_graph.bind("dicl", LIFECYCLE_NAMESPACE)
    instance_graph.bind("bot", BOT_NAMESPACE)
    instance_graph.bind("geo", GEO_NAMESPACE)
    return instance_graph


def _add_units_info_to_graph(ifc):
    units = ifc.by_type("IfcUnitAssignment")
    ic(units[0].get_info())


def tuple_to_decimal_latitude_or_longitude(coordinate_tuple: tuple) -> float:
    degrees, minutes, seconds, fractional_part = coordinate_tuple
    decimal_coordinate = (
        degrees
        + (minutes / 60)
        + (seconds / 3600)
        + (fractional_part / (3600 * 1000000))
    )
    return decimal_coordinate


def add_entity_guid_and_label_info_to_graph(ifc_file, graph: Graph, entity_type: str):
    entities = ifc_file.by_type(entity_type)
    for entity in entities:
        if entity_type == "IfcProject":
            graph.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                    RDF.type,
                    LIFECYCLE_NAMESPACE.Project,
                )
            )
        elif entity_type == "IfcSite":
            graph.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                    RDF.type,
                    BOT_NAMESPACE.Site,
                )
            )
            graph.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                    GEO_NAMESPACE.lat,
                    Literal(
                        f"{tuple_to_decimal_latitude_or_longitude(entity.RefLatitude)}",
                        datatype=XSD.float,
                    ),
                )
            )
            graph.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                    GEO_NAMESPACE.long,
                    Literal(
                        f"{tuple_to_decimal_latitude_or_longitude(entity.RefLongitude)}",
                        datatype=XSD.float,
                    ),
                )
            )
        elif entity_type == "IfcBuilding":
            graph.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                    RDF.type,
                    BOT_NAMESPACE.Building,
                )
            )
        elif entity_type == "IfcBuildingStorey":
            graph.add(
                (
                    URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                    RDF.type,
                    BOT_NAMESPACE.Storey,
                )
            )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasGlobalID,
                Literal(f"{entity.GlobalId}"),
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasLabel,
                Literal(f"{entity.Name}"),
            )
        )


def create_rdf_graph_from_ifc(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file)
    rdf_model = initialize_graph()
    entity_types_list = ["ifcProject", "ifcSite", "ifcBuilding", "ifcBuildingStorey"]
    for entity_type in entity_types_list:
        add_entity_guid_and_label_info_to_graph(
            ifc_model, rdf_model, entity_type=entity_type
        )
    return rdf_model
