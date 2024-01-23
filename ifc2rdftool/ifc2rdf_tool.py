import ifcopenshell
import ifcopenshell.util.element
from icecream import ic
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

from ifc2rdftool.building_info import add_building_info_to_graph
from ifc2rdftool.door_info import add_door_info_to_graph
from ifc2rdftool.graph_resources import (BEO_NAMESPACE, BOT_NAMESPACE,
                                         CORE_NAMESPACE, DICM_NAMESPACE,
                                         DICV_NAMESPACE, GEO_NAMESPACE,
                                         INSTANCE_NAMESPACE)
from ifc2rdftool.roof_info import add_roof_info_to_graph
from ifc2rdftool.site_info import add_site_info_to_graph
from ifc2rdftool.slab_info import add_slab_info_to_graph
from ifc2rdftool.space_info import add_space_info_to_graph
from ifc2rdftool.storey_info import add_storey_info_to_graph
from ifc2rdftool.wall_info import add_wall_info_to_graph
from ifc2rdftool.windows_info import add_windows_info_to_graph


def initialize_graph() -> Graph:
    instance_graph = Graph()
    instance_graph.bind("inst", INSTANCE_NAMESPACE)
    instance_graph.bind("core", CORE_NAMESPACE)
    instance_graph.bind("bot", BOT_NAMESPACE)
    instance_graph.bind("geo", GEO_NAMESPACE)
    instance_graph.bind("dicm", DICM_NAMESPACE)
    instance_graph.bind("beo", BEO_NAMESPACE)
    instance_graph.bind("dicv", DICV_NAMESPACE)
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
    if entity.Name:
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
    for entity in entities:
        add_entity_global_id_and_label_info_to_graph(entity, graph)
        if entity_type == "IfcSite":
            add_site_info_to_graph(entity, graph)
        elif entity_type == "IfcBuilding":
            add_building_info_to_graph(entity, graph)
        elif entity_type == "IfcBuildingStorey":
            add_storey_info_to_graph(entity, graph)
        elif entity_type in ["IfcWall", "IfcWallStandardCase"]:
            add_wall_info_to_graph(entity, graph)
        elif entity_type == "IfcSlab":
            add_slab_info_to_graph(entity, graph)
        elif entity_type == "IfcSpace":
            add_space_info_to_graph(entity, graph)
        elif entity_type == "IfcWindow":
            add_windows_info_to_graph(entity, graph)
        elif entity_type == "IfcDoor":
            add_door_info_to_graph(entity, graph)
        elif entity_type == "IfcRoof":
            add_roof_info_to_graph(entity, graph)


def get_all_entity_types_from_project_decomposition(ifc):
    project = ifc.by_type("IfcProject")[0]
    ifc_entities = ifcopenshell.util.element.get_decomposition(project)
    entity_types_list = []
    for entity in ifc_entities:
        entity_types_list.append(entity.is_a())
    return set(entity_types_list)


def create_rdf_graph_from_ifc(ifc_model):
    rdf_model = initialize_graph()
    project = ifc_model.by_type("IfcProject")[0]
    if project:
        add_project_info_to_graph(project, rdf_model)
        ifc_entity_types = get_all_entity_types_from_project_decomposition(ifc_model)
        for entity_type in ifc_entity_types:
            add_entity_info_to_graph(ifc_model, rdf_model, entity_type=entity_type)
    return rdf_model


def create_rdf_graph_from_ifc_file_path(ifc_file_path):
    ifc_model = ifcopenshell.open(ifc_file_path)
    return create_rdf_graph_from_ifc(ifc_model)
