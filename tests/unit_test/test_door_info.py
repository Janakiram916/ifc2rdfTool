from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.door_info import add_door_info_to_graph
from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.wall_info import get_element_properties
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.door_info.get_element_material_constituent_info")
@mock.patch("ifc2rdftool.door_info.get_element_properties")
def test_should_return_door_info_without_materials_and_property_data(
    mock_property_function, mock_constituents_func
) -> None:
    test_graph = initialize_graph()
    test_door_entity = TEST_IFC_FILE.by_type("IfcDoor")[0]
    add_door_info_to_graph(test_door_entity, test_graph)
    expected_graph_str = f"""
            {PREFIXES}
            inst:2rvVZuy3X0l9ATwUENTjYJ a beo:Door .
            inst:04XCdhzWXDtBhVSPQ7KoNt bot:containsElement inst:2rvVZuy3X0l9ATwUENTjYJ .
            """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_constituents_func.assert_called_once_with(test_door_entity, test_graph)
    mock_property_function.assert_called_once_with(test_door_entity, test_graph)


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
    test_door_entity = TEST_IFC_FILE.by_type("IfcDoor")[0]
    get_element_properties(test_door_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}

        inst:2rvVZuy3X0l9ATwUENTjYJ dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB ,
            inst:2rvVZuy3X0l9ATwV2NTYSe,
            inst:2rvVZuy3X0l9ATwUENTYSe.

        inst:2rvVZuy3X0l9ATwV2NTibB a dicv:Property ;
            core:hasLabel "ThermalTransmittance" ;
            core:hasValue "test_value1" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwV2NTibB" .

        inst:2rvVZuy3X0l9ATwV2NTYSe a dicv:Property ;
            core:hasLabel "Width" ;
            core:hasValue "test_value2" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwV2NTYSe" .

        inst:2rvVZuy3X0l9ATwUENTYSe a dicv:Property ;
            core:hasLabel "Thermal Resistance (R)" ;
            core:hasValue "test_value3" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwUENTYSe" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    assert mock_psets.call_count == 1
    assert mock_guid.call_count == 3
