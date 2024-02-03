from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.windows_info import get_element_material_constituent_info
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch(
    "ifc2rdftool.windows_info.get_multiple_guids",
    return_value=[
        "1a8Aef4WT5O95P1duyJUJM",
        "1JiIoLE5XAvx1zVHUdIyGn",
        "213gwkWvf7bv0837WjMTfN",
    ],
)
@mock.patch(
    "ifc2rdftool.windows_info.get_valid_guid",
    side_effect=[
        "2rvVZuy3X0l9ATwV2NTibB",
    ],
)
@mock.patch(
    "ifc2rdftool.wall_info.get_valid_guid",
    side_effect=[
        "1InbJU1uf1NgTLNghGHC45",
        "1InbJU1uf1NgTLNghGHC46",
        "1InbJU1uf1NgTLNghGHC47",
    ],
)
def test_should_return_graph_with_door_layer_data_when_entity_type_is_ifc_window(
    mocked_material_guid, mocked_constituent_guid, mocker_layer_set_guid
) -> None:
    test_graph = initialize_graph()
    test_door_entity = TEST_IFC_FILE.by_type("IfcDoor")[0]
    get_element_material_constituent_info(test_door_entity, test_graph)
    expected_graph = Graph().parse(
        source="tests/integration_test/test_resources/test_door_constituent.ttl",
        format="turtle",
    )
    assert isomorphic(test_graph, expected_graph)
    mocked_material_guid.assert_called()
    mocked_constituent_guid.assert_called()
    mocker_layer_set_guid.assert_called_once()
