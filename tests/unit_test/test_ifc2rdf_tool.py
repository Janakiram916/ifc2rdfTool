import ifcopenshell
from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import (add_entity_guid_and_label_info_to_graph,
                                      initialize_graph,
                                      tuple_to_decimal_latitude_or_longitude)

_TEST_IFC_FILE_PATH = "tests/test_resources/Demonstration_Model_V1_DTV_4.ifc"
_TEST_IFC_FILE = ifcopenshell.open(_TEST_IFC_FILE_PATH)


def test_should_return_graph_with_project_data_when_entity_type_is_ifc_project() -> (
    None
):
    test_graph = initialize_graph()
    add_entity_guid_and_label_info_to_graph(
        _TEST_IFC_FILE, test_graph, entity_type="IfcProject"
    )
    expected_graph_str = """
    @prefix dicl: <https://w3id.org/digitalconstruction/0.5/Lifecycle#> .
    @prefix inst: <https://w3id.org/digitalconstruction/instance#> .
    
    inst:04XCdhzWXDtBhVSPPuhCyZ a dicl:Project ;
    dicl:hasGlobalID "04XCdhzWXDtBhVSPPuhCyZ" ;
    dicl:hasLabel "0001" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)


def test_should_return_graph_with_units_data_when_ifc_file_is_inputted() -> None:
    pass


def test_should_return_graph_with_site_data_when_entity_type_is_ifc_site() -> None:
    test_graph = initialize_graph()
    add_entity_guid_and_label_info_to_graph(
        _TEST_IFC_FILE, test_graph, entity_type="IfcSite"
    )
    expected_graph_str = f"""
        {PREFIXES}
        inst:04XCdhzWXDtBhVSPPuhCyX a bot:Site ;
            dicl:hasGlobalID "04XCdhzWXDtBhVSPPuhCyX" ;
            dicl:hasLabel "Default" ;
            geo:lat "51.034439086666666"^^xsd:float ;
            geo:long "13.72202587111111"^^xsd:float .
        """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)


def test_should_return_longitude_decimal_when_longitude_tuple_inputted():
    test_latitude = (13, 43, 19, 0)
    expected_latitude = 13.721944444444444
    actual_latitude = tuple_to_decimal_latitude_or_longitude(test_latitude)
    assert actual_latitude == expected_latitude


def test_should_return_building_data_when_entity_type_is_ifc_building() -> None:
    test_graph = initialize_graph()
    add_entity_guid_and_label_info_to_graph(
        _TEST_IFC_FILE, test_graph, entity_type="IfcBuilding"
    )
    expected_graph_str = f"""
        {PREFIXES}
        inst:04XCdhzWXDtBhVSPPuhCyY a bot:Building ;
            dicl:hasGlobalID "04XCdhzWXDtBhVSPPuhCyY" ;
            dicl:hasLabel "CIB" .
        """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)


def test_should_return_graph_with_storey_data_when_entity_type_is_ifc_building_storey() -> (
    None
):
    test_graph = initialize_graph()
    add_entity_guid_and_label_info_to_graph(
        _TEST_IFC_FILE, test_graph, entity_type="IfcBuildingStorey"
    )
    expected_graph_path = "tests/test_resources/test_storey.ttl"
    expected_graph = Graph().parse(source=expected_graph_path, format="turtle")
    assert isomorphic(test_graph, expected_graph)
