# pylint: disable=C0114
import ifcopenshell
from icecream import ic
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

from ifc2rdftool.graph_resources import INSTANCE_NAMESPACE, LIFECYCLE_NAMESPACE


def _initialize_graph() -> Graph:
    instance_graph = Graph()
    instance_graph.bind("inst", INSTANCE_NAMESPACE)
    instance_graph.bind("dicl", LIFECYCLE_NAMESPACE)
    return instance_graph


def _add_project_info_to_graph(ifc_file, graph: Graph):
    ic(type(ifc_file))
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


def _add_site_info_to_graph():
    pass


def _create_rdf_graph_from_ifc(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file)
    rdf_model = _initialize_graph()
    _add_project_info_to_graph(ifc_model, rdf_model)


if __name__ == "__main__":
    pass
