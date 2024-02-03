from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.wall_info import get_element_layer_info
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch(
    "ifc2rdftool.wall_info.get_multiple_guids",
    return_value=[
        "1a8Aef4WT5O95P1duyJUJM",
        "1JiIoLE5XAvx1zVHUdIyGn",
        "213gwkWvf7bv0837WjMTfN",
    ],
)
@mock.patch(
    "ifc2rdftool.wall_info.get_valid_guid",
    side_effect=[
        "2rvVZuy3X0l9ATwV2NTibB",
        "29m76ZKSP4n8xpWQ5lKvUQ",
        "1XVbyL0DzCVOyewmt2whMj",
        "1vYs0UNEb6LB1yYXDqLDIH",
        "1InbJU1uf1NgTLNghGHC45",
        "1InbJU1uf1NgTLNghGHC46",
        "1InbJU1uf1NgTLNghGHC47",
    ],
)
def test_should_return_graph_with_wall_layer_data_when_entity_type_is_ifc_wall(
    mocked_layers_guid, mocker_layer_set_guid
) -> None:
    test_graph = initialize_graph()
    test_building_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    get_element_layer_info(test_building_entity, test_graph)
    expected_graph = Graph().parse(
        source="tests/integration_test/test_resources/test_wall_layer.ttl",
        format="turtle",
    )
    assert isomorphic(test_graph, expected_graph)
    mocked_layers_guid.assert_called()
    mocker_layer_set_guid.assert_called_once()
