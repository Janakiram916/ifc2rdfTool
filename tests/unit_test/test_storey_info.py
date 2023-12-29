from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.storey_info import add_storey_info_to_graph
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


def test_should_return_graph_with_storey_data_when_entity_type_is_ifc_building_storey() -> (
    None
):
    test_graph = initialize_graph()
    test_storey_entities = TEST_IFC_FILE.by_type("IfcBuildingStorey")
    for test_storey in test_storey_entities:
        add_storey_info_to_graph(test_storey, test_graph)
    expected_graph_path = "tests/test_resources/test_storey.ttl"
    expected_graph = Graph().parse(source=expected_graph_path, format="turtle")
    assert isomorphic(test_graph, expected_graph)
