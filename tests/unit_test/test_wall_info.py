from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.wall_info import (add_wall_info_to_graph,
                                   create_property_triple,
                                   get_element_layer_info, get_multiple_guids,
                                   get_valid_guid, get_wall_properties)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.wall_info.get_element_layer_info")
@mock.patch("ifc2rdftool.wall_info.get_wall_properties")
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
    ],
)
def test_should_return_graph_with_wall_layer_data_when_entity_type_is_ifc_wall(
    mocked_layers_guid, mocker_layer_set_guid
) -> None:
    test_graph = initialize_graph()
    test_building_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    get_element_layer_info(test_building_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        
        inst:0mhevRo9r5X8JNSuTZNOZH dicm:hasLayerSet inst:2rvVZuy3X0l9ATwV2NTibB .
        
        inst:1JiIoLE5XAvx1zVHUdIyGn a dicm:Layer ;
            dicm:hasMaterial "Concrete, Lightweight" ;
            dicv:hasProperty inst:1XVbyL0DzCVOyewmt2whMj ;
            core:hasLabel "Concrete, Lightweight" .
            
        inst:1a8Aef4WT5O95P1duyJUJM a dicm:Layer ;
            dicm:hasMaterial "Brick, Common" ;
            dicv:hasProperty inst:29m76ZKSP4n8xpWQ5lKvUQ ;
            core:hasLabel "Brick, Common" .
        
        inst:1XVbyL0DzCVOyewmt2whMj a dicv:Property ;
            core:hasLabel "LayerThickness" ;
            core:hasValue 2.032e+02 .
        
        inst:1vYs0UNEb6LB1yYXDqLDIH a dicv:Property ;
            core:hasLabel "LayerThickness" ;
            core:hasValue 1.27e+01 .

        inst:213gwkWvf7bv0837WjMTfN a dicm:Layer ;
            dicm:hasMaterial "Gypsum Wall Board" ;
            dicv:hasProperty inst:1vYs0UNEb6LB1yYXDqLDIH ;
            core:hasLabel "Gypsum Wall Board" .
        
        inst:29m76ZKSP4n8xpWQ5lKvUQ a dicv:Property ;
            core:hasLabel "LayerThickness" ;
            core:hasValue 1.016e+02 .

        inst:2rvVZuy3X0l9ATwV2NTibB a dicm:LayerSet ;
            dicm:NumberOfLayers 3 ;
            dicm:hasLayer inst:1JiIoLE5XAvx1zVHUdIyGn ,
                inst:1a8Aef4WT5O95P1duyJUJM ,
                inst:213gwkWvf7bv0837WjMTfN ;
            core:hasName "Basic Wall:Exterior_Wall - 101.6mm Brick + 203.2mm Concrete + 12.7mm Gypsum Plaster" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mocked_layers_guid.assert_called()
    mocker_layer_set_guid.assert_called_once()


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
    get_wall_properties(test_wall_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB.
        inst:2rvVZuy3X0l9ATwV2NTibB a dicv:Property ;
            core:hasLabel "ThermalTransmittance" ;
            core:hasValue "test_value1" .
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTYSe.
        inst:2rvVZuy3X0l9ATwV2NTYSe a dicv:Property ;
            core:hasLabel "Length" ;
            core:hasValue "test_value2" .
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwUENTYSe.
        inst:2rvVZuy3X0l9ATwUENTYSe a dicv:Property ;
            core:hasLabel "Thermal Resistance (R)" ;
            core:hasValue "test_value3" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    assert mock_psets.call_count == 1
    assert mock_guid.call_count == 3


@mock.patch(
    "ifc2rdftool.wall_info.get_valid_guid", return_value="2rvVZuy3X0l9ATwV2NTibB"
)
def test_should_return_property_triple(mock_guid) -> None:
    test_graph = initialize_graph()
    test_wall_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    create_property_triple(
        "test_property", "test_value", test_wall_entity.GlobalId, test_graph
    )
    expected_graph_str = f"""
        {PREFIXES}
        
        inst:0mhevRo9r5X8JNSuTZNOZH dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB.
        inst:2rvVZuy3X0l9ATwV2NTibB a dicv:Property ;
            core:hasLabel "test_property" ;
            core:hasValue "test_value" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_guid.assert_called_once()
