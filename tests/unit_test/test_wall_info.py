from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.wall_info import (add_wall_info_to_graph,
                                   get_element_layer_info)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.wall_info.get_element_layer_info")
def test_should_return_graph_with_wall_data_when_entity_type_is_ifc_wall(
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


@mock.patch(
    "ifc2rdftool.wall_info.get_multiple_guids",
    return_value=[
        "1a8Aef4WT5O95P1duyJUJM",
        "1JiIoLE5XAvx1zVHUdIyGn",
        "213gwkWvf7bv0837WjMTfN",
    ],
)
@mock.patch("ifc2rdftool.wall_info.LAYER_SET_GUID", new="2rvVZuy3X0l9ATwV2NTibB")
def test_should_return_graph_with_wall_layer_data_when_entity_type_is_ifc_wall(
    mocked_layers_guid,
) -> None:
    test_graph = initialize_graph()
    test_building_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
    get_element_layer_info(test_building_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        
        inst:0mhevRo9r5X8JNSuTZNOZH dicm:hasLayerSet inst:2rvVZuy3X0l9ATwV2NTibB .
        
        inst:1JiIoLE5XAvx1zVHUdIyGn a dicm:Layer ;
            dicm:hasMaterial "Concrete, Lightweight" ;
            dicm:hasThickness 2.032e+02 ;
            core:hasLabel "Concrete, Lightweight" .
            
        inst:1a8Aef4WT5O95P1duyJUJM a dicm:Layer ;
            dicm:hasMaterial "Brick, Common" ;
            dicm:hasThickness 1.016e+02 ;
            core:hasLabel "Brick, Common" .

        inst:213gwkWvf7bv0837WjMTfN a dicm:Layer ;
            dicm:hasMaterial "Gypsum Wall Board" ;
            dicm:hasThickness 1.27e+01 ;
            core:hasLabel "Gypsum Wall Board" .

        inst:2rvVZuy3X0l9ATwV2NTibB a dicm:LayerSet ;
            dicm:NumberOfLayers 3 ;
            dicm:hasLayer inst:1JiIoLE5XAvx1zVHUdIyGn ,
                inst:1a8Aef4WT5O95P1duyJUJM ,
                inst:213gwkWvf7bv0837WjMTfN ;
            core:hasName "Basic Wall:Exterior_Wall - 101.6mm Brick + 203.2mm Concrete + 12.7mm Gypsum Plaster" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mocked_layers_guid.assert_called_once()
