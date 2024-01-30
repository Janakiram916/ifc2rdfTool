from unittest import mock

from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.space_info import add_space_info_to_graph
from ifc2rdftool.wall_info import get_element_properties
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


@mock.patch("ifc2rdftool.space_info.get_element_properties")
def test_should_return_space_info_without_property_data(
    mock_property_function,
) -> None:
    test_graph = initialize_graph()
    test_space_entity = TEST_IFC_FILE.by_type("IfcSpace")[4]
    add_space_info_to_graph(test_space_entity, test_graph)
    expected_graph_str = f"""
            {PREFIXES}
            inst:1RUXumxMXEpBDqH_kH6Prv a bot:Space .
            """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    mock_property_function.assert_called_once_with(test_space_entity, test_graph)


@mock.patch("ifcopenshell.util.element.get_psets")
@mock.patch("ifc2rdftool.wall_info.get_valid_guid")
def test_should_return_space_properties(mock_guid, mock_psets) -> None:
    mock_guid.side_effect = [
        "2rvVZuy3X0l9ATwV2NTibB",
        "2rvVZuy3X0l9ATwV2NTYSe",
    ]
    mock_psets.return_value = {
        "Pset_SpaceCommon": {"IsExternal": "test_value1"},
        "Qto_SpaceBaseQuantities": {"Height": "test_value2"},
    }
    test_graph = initialize_graph()
    test_space_entity = TEST_IFC_FILE.by_type("IfcSpace")[4]
    get_element_properties(test_space_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}

        inst:1RUXumxMXEpBDqH_kH6Prv dicv:hasProperty inst:2rvVZuy3X0l9ATwV2NTibB ,
            inst:2rvVZuy3X0l9ATwV2NTYSe.

        inst:2rvVZuy3X0l9ATwV2NTibB a dicv:Property ;
            core:hasLabel "IsExternal" ;
            core:hasValue "test_value1" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwV2NTibB" .

        inst:2rvVZuy3X0l9ATwV2NTYSe a dicv:Property ;
            core:hasLabel "Height" ;
            core:hasValue "test_value2" ;
            core:hasGlobalID "2rvVZuy3X0l9ATwV2NTYSe" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
    assert mock_psets.call_count == 1
    assert mock_guid.call_count == 2
