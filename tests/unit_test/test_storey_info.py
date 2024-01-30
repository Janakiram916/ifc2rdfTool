from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.storey_info import (add_storey_info_to_graph,
                                     get_relationship_with_spaces)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.storey_info.get_relationship_with_spaces")
def test_should_return_graph_with_storey_data_when_entity_type_is_ifc_building_storey(
    mock_spaces,
) -> None:
    test_graph = initialize_graph()
    test_storey_entities = TEST_IFC_FILE.by_type("IfcBuildingStorey")
    for test_storey in test_storey_entities:
        add_storey_info_to_graph(test_storey, test_graph)
    expected_graph_path = "tests/unit_test/test_resources/test_storey.ttl"
    expected_graph = Graph().parse(source=expected_graph_path, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_spaces.assert_called()


def test_should_return_relationship_with_spatial_elements() -> None:
    test_graph = initialize_graph()
    test_storey_entity = TEST_IFC_FILE.by_type("IfcBuildingStorey")[0]
    get_relationship_with_spaces(test_storey_entity, test_graph)
    expected_graph_str = """
    @prefix bot: <https://w3id.org/bot#> .
    @prefix inst: <https://w3id.org/digitalconstruction/instance#> .
    
    inst:04XCdhzWXDtBhVSPQ7KoNt bot:hasSpace 
        <https://w3id.org/digitalconstruction/instance#03tkq$Dnf8jOaNsHm9RsT2>,
        <https://w3id.org/digitalconstruction/instance#03tkq$Dnf8jOaNsHm9RsTO>,
        <https://w3id.org/digitalconstruction/instance#03tkq$Dnf8jOaNsHm9RsTS>,
        <https://w3id.org/digitalconstruction/instance#03tkq$Dnf8jOaNsHm9RsTU> .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
