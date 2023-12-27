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


def add_project_info_to_graph(ifc_file, graph: Graph):
    projects = ifc_file.by_type("IfcProject")
    for project in projects:
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{project.GlobalId}"),
                RDF.type,
                LIFECYCLE_NAMESPACE.Project,
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{project.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasGlobalID,
                Literal(f"{project.GlobalId}"),
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{project.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasLabel,
                Literal(f"{project.Name}"),
            )
        )


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


def add_site_info_to_graph(ifc_file, graph: Graph):
    sites = ifc_file.by_type("IfcSite")
    for site in sites:
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{site.GlobalId}"),
                RDF.type,
                BOT_NAMESPACE.Site,
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{site.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasGlobalID,
                Literal(f"{site.GlobalId}"),
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{site.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasLabel,
                Literal(f"{site.Name}"),
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{site.GlobalId}"),
                GEO_NAMESPACE.lat,
                Literal(
                    f"{tuple_to_decimal_latitude_or_longitude(site.RefLatitude)}",
                    datatype=XSD.float,
                ),
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{site.GlobalId}"),
                GEO_NAMESPACE.long,
                Literal(
                    f"{tuple_to_decimal_latitude_or_longitude(site.RefLongitude)}",
                    datatype=XSD.float,
                ),
            )
        )


def add_building_info_to_graph(ifc_file, graph: Graph):
    buildings = ifc_file.by_type("IfcBuilding")
    for building in buildings:
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{building.GlobalId}"),
                RDF.type,
                BOT_NAMESPACE.Building,
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{building.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasGlobalID,
                Literal(f"{building.GlobalId}"),
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{building.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasLabel,
                Literal(f"{building.Name}"),
            )
        )


def add_storey_info_to_graph(ifc_file, graph: Graph):
    storeys = ifc_file.by_type("IfcBuildingStorey")
    for storey in storeys:
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{storey.GlobalId}"),
                RDF.type,
                BOT_NAMESPACE.Storey,
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{storey.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasGlobalID,
                Literal(f"{storey.GlobalId}"),
            )
        )
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{storey.GlobalId}"),
                LIFECYCLE_NAMESPACE.hasLabel,
                Literal(f"{storey.Name}"),
            )
        )


def _create_rdf_graph_from_ifc(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file)
    rdf_model = initialize_graph()
    add_project_info_to_graph(ifc_model, rdf_model)
    add_site_info_to_graph(ifc_model, rdf_model)
    add_building_info_to_graph(ifc_model, rdf_model)
    add_storey_info_to_graph(ifc_model, rdf_model)
    return rdf_model
