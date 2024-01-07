from unittest import mock

import ifcopenshell.util.element
from icecream import ic
from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.slab_info import add_slab_info_to_graph
from ifc2rdftool.wall_info import (get_element_layer_info,
                                   get_element_properties)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.slab_info.get_element_layer_info")
@mock.patch("ifc2rdftool.slab_info.get_element_properties")
def test_should_return_slab_info_without_layers_and_property_data(
    mock_property_function,
    mock_layers_function,
) -> None:
    test_graph = initialize_graph()
    test_slab_entity = TEST_IFC_FILE.by_type("IfcSlab")[0]
    add_slab_info_to_graph(test_slab_entity, test_graph)
    expected_graph_str = f"""
            {PREFIXES}
            inst:3IgqlyNZb9CR1JNQVbt_lX a beo:Slab .
            inst:04XCdhzWXDtBhVSPQ7KoNt bot:containsElement inst:3IgqlyNZb9CR1JNQVbt_lX .
            """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_layers_function.assert_called_once_with(test_slab_entity, test_graph)
    mock_property_function.assert_called_once_with(test_slab_entity, test_graph)


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
def test_should_return_graph_with_slab_layer_data_when_entity_type_is_ifc_slab(
    mocked_layers_guid, mocker_layer_set_guid
) -> None:
    test_graph = initialize_graph()
    test_building_entity = TEST_IFC_FILE.by_type("IfcSlab")[0]
    get_element_layer_info(test_building_entity, test_graph)
    expected_graph = Graph().parse(
        source="tests/test_resources/test_slab_layer.ttl", format="turtle"
    )
    assert isomorphic(test_graph, expected_graph)
    mocked_layers_guid.assert_called()
    mocker_layer_set_guid.assert_called_once()


@mock.patch("ifcopenshell.util.element.get_psets")
@mock.patch("ifc2rdftool.wall_info.get_valid_guid")
def test_should_return_slab_properties(mock_guid, mock_psets) -> None:
    mock_guid.side_effect = [
        "2rvVZuy3X0l9ATwV2NTibB",
        "2rvVZuy3X0l9ATwV2NTYSe",
        "2rvVZuy3X0l9ATwUENTYSe",
    ]
    mock_psets.return_value = {
        "Pset_SlabCommon": {"ThermalTransmittance": "test_value1"},
        "Qto_SlabBaseQuantities": {"Width": "test_value2"},
        "Analytical Properties": {"Thermal Resistance (R)": "test_value3"},
    }
    test_graph = initialize_graph()
    test_wall_entity = TEST_IFC_FILE.by_type("IfcSlab")[0]
    get_element_properties(test_wall_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}

        inst:3IgqlyNZb9CR1JNQVbt_lX dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB ,
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
