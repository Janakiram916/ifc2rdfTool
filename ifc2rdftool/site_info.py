import ifcopenshell
import ifcopenshell.util.element
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

from ifc2rdftool.graph_resources import (BOT_NAMESPACE, CORE_NAMESPACE,
                                         GEO_NAMESPACE, INSTANCE_NAMESPACE)


def tuple_to_decimal_latitude_or_longitude(coordinate_tuple: tuple) -> float:
    degrees, minutes, seconds, fractional_part = coordinate_tuple
    decimal_coordinate = (
        degrees
        + (minutes / 60)
        + (seconds / 3600)
        + (fractional_part / (3600 * 1000000))
    )
    return decimal_coordinate


def add_site_info_to_graph(site_entity, graph: Graph):
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{site_entity.GlobalId}"),
            RDF.type,
            BOT_NAMESPACE.Site,
        )
    )
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{site_entity.GlobalId}"),
            GEO_NAMESPACE.lat,
            Literal(
                f"{tuple_to_decimal_latitude_or_longitude(site_entity.RefLatitude)}",
                datatype=XSD.float,
            ),
        )
    )
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{site_entity.GlobalId}"),
            GEO_NAMESPACE.long,
            Literal(
                f"{tuple_to_decimal_latitude_or_longitude(site_entity.RefLongitude)}",
                datatype=XSD.float,
            ),
        )
    )
    decomposition = ifcopenshell.util.element.get_aggregate(site_entity)
    if decomposition:
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{decomposition.GlobalId}"),
                CORE_NAMESPACE.hasSite,
                URIRef(f"{INSTANCE_NAMESPACE}{site_entity.GlobalId}"),
            )
        )
