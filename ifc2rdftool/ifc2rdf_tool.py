import ifcopenshell
import ifcopenshell.util.element
from icecream import ic
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

from ifc2rdftool.building_info import add_building_info_to_graph
from ifc2rdftool.graph_resources import (BOT_NAMESPACE, CORE_NAMESPACE,
                                         DICM_NAMESPACE, GEO_NAMESPACE,
                                         INSTANCE_NAMESPACE)
from ifc2rdftool.site_info import add_site_info_to_graph
from ifc2rdftool.storey_info import add_storey_info_to_graph
from ifc2rdftool.wall_info import add_wall_info_to_graph


def initialize_graph() -> Graph:
    instance_graph = Graph()
    instance_graph.bind("inst", INSTANCE_NAMESPACE)
    instance_graph.bind("core", CORE_NAMESPACE)
    instance_graph.bind("bot", BOT_NAMESPACE)
    instance_graph.bind("geo", GEO_NAMESPACE)
    instance_graph.bind("dicm", DICM_NAMESPACE)
    return instance_graph


def _add_units_info_to_graph(ifc):
    units = ifc.by_type("IfcUnitAssignment")
    ic(units[0].get_info())


def add_entity_global_id_and_label_info_to_graph(entity, graph: Graph):
    # ic(entity.get_info())
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
            CORE_NAMESPACE.hasGlobalID,
            Literal(f"{entity.GlobalId}"),
        )
    )
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
            CORE_NAMESPACE.hasLabel,
            Literal(f"{entity.Name}"),
        )
    )
    if "LongName" in entity.get_info().keys():
        graph.add(
            (
                URIRef(f"{INSTANCE_NAMESPACE}{entity.GlobalId}"),
                CORE_NAMESPACE.hasName,
                Literal(f"{entity.LongName}"),
            )
        )


def add_project_info_to_graph(project_entity, graph: Graph):
    graph.add(
        (
            URIRef(f"{INSTANCE_NAMESPACE}{project_entity.GlobalId}"),
            RDF.type,
            CORE_NAMESPACE.Project,
        )
    )
    add_entity_global_id_and_label_info_to_graph(project_entity, graph)


def add_entity_info_to_graph(ifc_file, graph: Graph, entity_type: str):
    entities = ifc_file.by_type(entity_type)
    if entity_type == "IfcSite":
        for entity in entities:
            add_site_info_to_graph(entity, graph)
    elif entity_type == "IfcBuilding":
        for entity in entities:
            add_building_info_to_graph(entity, graph)
    elif entity_type == "IfcBuildingStorey":
        for entity in entities:
            add_storey_info_to_graph(entity, graph)
    elif entity_type == "IfcWall":
        for entity in entities:
            add_wall_info_to_graph(entity, graph)


def create_rdf_graph_from_ifc(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file)
    rdf_model = initialize_graph()
    project = ifc_model.by_type("IfcProject")[0]
    add_project_info_to_graph(project, rdf_model)
    ifc_entities = ifcopenshell.util.element.get_decomposition(project)
    entity_types_list = []
    for entity in ifc_entities:
        add_entity_global_id_and_label_info_to_graph(entity, rdf_model)
        entity_types_list.append(entity.is_a())
    entity_types_list.sort()
    # ic(set(entity_types_list))
    for entity_type in entity_types_list:
        add_entity_info_to_graph(ifc_model, rdf_model, entity_type=entity_type)
    return rdf_model
