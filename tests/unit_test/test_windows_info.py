from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.wall_info import get_element_properties
from ifc2rdftool.windows_info import (add_windows_info_to_graph,
                                      get_element_material_constituent_info)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.windows_info.get_element_material_constituent_info")
@mock.patch("ifc2rdftool.windows_info.get_element_properties")
def test_should_return_window_info_without_materials_and_property_data(
    mock_property_function, mock_constituents_func
) -> None:
    test_graph = initialize_graph()
    test_window_entity = TEST_IFC_FILE.by_type("IfcWindow")[0]
    add_windows_info_to_graph(test_window_entity, test_graph)
    expected_graph_str = f"""
            {PREFIXES}
            inst:2rvVZuy3X0l9ATwUENTYQY a beo:Window .
            inst:04XCdhzWXDtBhVSPQ7KoNt bot:containsElement inst:2rvVZuy3X0l9ATwUENTYQY .
            """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_constituents_func.assert_called_once_with(test_window_entity, test_graph)
    mock_property_function.assert_called_once_with(test_window_entity, test_graph)


@mock.patch("ifcopenshell.util.element.get_psets")
@mock.patch("ifc2rdftool.wall_info.get_valid_guid")
def test_should_return_window_properties(mock_guid, mock_psets) -> None:
    mock_guid.side_effect = [
        "2rvVZuy3X0l9ATwV2NTibB",
        "2rvVZuy3X0l9ATwV2NTYSe",
        "2rvVZuy3X0l9ATwUENTYSe",
    ]
    mock_psets.return_value = {
        "Pset_WindowCommon": {"ThermalTransmittance": "test_value1"},
        "Qto_WindowBaseQuantities": {"Width": "test_value2"},
        "Analytical Properties": {"Thermal Resistance (R)": "test_value3"},
    }
    test_graph = initialize_graph()
    test_window_entity = TEST_IFC_FILE.by_type("IfcWindow")[0]
    get_element_properties(test_window_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}

        inst:2rvVZuy3X0l9ATwUENTYQY dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB ,
            inst:2rvVZuy3X0l9ATwV2NTYSe,
            inst:2rvVZuy3X0l9ATwUENTYSe.

        inst:2rvVZuy3X0l9ATwV2NTibB a dicv:Property ;
            core:hasLabel "ThermalTransmittance" ;
            core:hasValue "test_value1" .

        inst:2rvVZuy3X0l9ATwV2NTYSe a dicv:Property ;
            core:hasLabel "Width" ;
            core:hasValue "test_value2" .

        inst:2rvVZuy3X0l9ATwUENTYSe a dicv:Property ;
            core:hasLabel "Thermal Resistance (R)" ;
            core:hasValue "test_value3" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    assert mock_psets.call_count == 1
    assert mock_guid.call_count == 3


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
def test_should_return_graph_with_window_layer_data_when_entity_type_is_ifc_window(
    mocked_material_guid, mocked_constituent_guid, mocker_layer_set_guid
) -> None:
    test_graph = initialize_graph()
    test_window_entity = TEST_IFC_FILE.by_type("IfcWindow")[0]
    get_element_material_constituent_info(test_window_entity, test_graph)
    expected_graph = Graph().parse(
        source="tests/unit_test/test_resources/test_window_constituent.ttl",
        format="turtle",
    )
    assert isomorphic(test_graph, expected_graph)
    mocked_material_guid.assert_called()
    mocked_constituent_guid.assert_called()
    mocker_layer_set_guid.assert_called_once()
