from unittest import mock

import ifcopenshell.util.element
from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.wall_info import (
    add_wall_info_to_graph,
    create_property_triple,
    get_element_properties,
    get_material_triples,
    get_multiple_guids,
    get_valid_guid,
)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.wall_info.get_element_layer_info")
@mock.patch("ifc2rdftool.wall_info.get_element_properties")
def test_should_return_graph_with_wall_data_when_entity_type_is_ifc_wall(
    mock_property_function,
    mock_layers_function,
) -> None:
    test_graph = initialize_graph()
    test_building_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    add_wall_info_to_graph(test_building_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        inst:0mhevRo9r5X8JNSuTZNOZH a beo:Wall ;
            bot:containsElement inst:2rvVZuy3X0l9ATwV2NTibB ;
            bot:containsElement inst:2rvVZuy3X0l9ATwV2NTYSe ;
            bot:containsElement inst:2rvVZuy3X0l9ATwUENTYSe ;
            bot:containsElement inst:2rvVZuy3X0l9ATwUENTibB .
        inst:04XCdhzWXDtBhVSPQ7KoNt bot:containsElement inst:0mhevRo9r5X8JNSuTZNOZH .
        """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_layers_function.assert_called_once_with(test_building_entity, test_graph)
    mock_property_function.assert_called_once_with(test_building_entity, test_graph)


def test_should_return_valid_guid() -> None:
    test_guid = get_valid_guid()
    assert "&" not in test_guid
    assert len(test_guid) == 22


def test_should_return_valid_list_of_guids() -> None:
    no_of_guids = 4
    test_guid_list = get_multiple_guids(no_of_guids)
    assert len(test_guid_list) == no_of_guids
    for guid in test_guid_list:
        assert "&" not in guid


@mock.patch("ifcopenshell.util.element.get_psets")
@mock.patch("ifc2rdftool.wall_info.get_valid_guid")
def test_should_return_wall_properties(mock_guid, mock_psets) -> None:
    mock_guid.side_effect = [
        "2rvVZuy3X0l9ATwV2NTibB",
        "2rvVZuy3X0l9ATwV2NTYSe",
        "2rvVZuy3X0l9ATwUENTYSe",
    ]
    mock_psets.return_value = {
        "Pset_WallCommon": {"ThermalTransmittance": "test_value1"},
        "Qto_WallBaseQuantities": {"Length": "test_value2"},
        "Analytical Properties": {"Thermal Resistance (R)": "test_value3"},
    }
    test_graph = initialize_graph()
    test_wall_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    get_element_properties(test_wall_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB.
        inst:2rvVZuy3X0l9ATwV2NTibB a dicv:Property ;
            core:hasLabel "ThermalTransmittance" ;
            core:hasValue "test_value1" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwV2NTibB" .
            
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTYSe.
        inst:2rvVZuy3X0l9ATwV2NTYSe a dicv:Property ;
            core:hasLabel "Length" ;
            core:hasValue "test_value2" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwV2NTYSe" .
            
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwUENTYSe.
        inst:2rvVZuy3X0l9ATwUENTYSe a dicv:Property ;
            core:hasLabel "Thermal Resistance (R)" ;
            core:hasValue "test_value3" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwUENTYSe" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    assert mock_psets.call_count == 1
    assert mock_guid.call_count == 3


@mock.patch("ifc2rdftool.wall_info.get_valid_guid", return_value="2rvVZuy3X0l9ATwV2NTibB")
def test_should_return_property_triple(mock_guid) -> None:
    test_graph = initialize_graph()
    test_wall_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    create_property_triple("test_property", "test_value", test_wall_entity.GlobalId, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB.
        inst:2rvVZuy3X0l9ATwV2NTibB a dicv:Property ;
            core:hasLabel "test_property" ;
            core:hasValue "test_value" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwV2NTibB" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_guid.assert_called_once()


@mock.patch("ifc2rdftool.wall_info.get_valid_guid", return_value="1InbJU1uf1NgTLNghGHCBy")
def test_should_return_material_data(mock_guid) -> None:
    test_graph = initialize_graph()
    test_layer_guid = "2rvVZuy3X0l9ATwV2NTibB"
    test_wall_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    test_material_entity = ifcopenshell.util.element.get_materials(test_wall_entity)[0]
    get_material_triples(test_layer_guid, test_material_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        
        inst:2rvVZuy3X0l9ATwV2NTibB dicm:hasMaterial inst:1InbJU1uf1NgTLNghGHCBy .
        inst:1InbJU1uf1NgTLNghGHCBy a dicm:Material ;
            core:hasLabel "Brick, Common" ;
            core:hasGlobalID "1InbJU1uf1NgTLNghGHCBy" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
