import ifcopenshell
from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.ifc2rdf_tool import (
    add_entity_global_id_and_label_info_to_graph, add_project_info_to_graph,
    get_all_entity_types_from_project_decomposition, initialize_graph)

TEST_IFC_FILE_PATH = "tests/unit_test/test_resources/Demonstration_Model_V1_DTV_4.ifc"
TEST_IFC_FILE = ifcopenshell.open(TEST_IFC_FILE_PATH)


def test_should_return_graph_with_project_data_when_entity_type_is_ifc_project() -> (
    None
):
    test_graph = initialize_graph()
    test_project_entity = TEST_IFC_FILE.by_type("IfcProject")[0]
    add_project_info_to_graph(test_project_entity, test_graph)
    expected_graph_str = """
    @prefix core: <https://w3id.org/digitalconstruction/core#> .
    @prefix inst: <https://w3id.org/digitalconstruction/instance#> .
    
    inst:04XCdhzWXDtBhVSPPuhCyZ a core:Project ;
    core:hasGlobalID "04XCdhzWXDtBhVSPPuhCyZ" ;
    core:hasName "Project Name" ;
    core:hasLabel "0001" .
    """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)


def test_should_return_ifc_entities_involved_in_project() -> None:
    test_ifc_model = TEST_IFC_FILE
    actual_ifc_entities = get_all_entity_types_from_project_decomposition(
        test_ifc_model
    )
    expected_ifc_entities = {
        "IfcBuilding",
        "IfcBuildingStorey",
        "IfcDoor",
        "IfcOpeningElement",
        "IfcRailing",
        "IfcRoof",
        "IfcSite",
        "IfcSlab",
        "IfcSpace",
        "IfcWall",
        "IfcWindow",
    }
    assert actual_ifc_entities == expected_ifc_entities


def test_should_return_id_and_name_of_ifc_entity() -> None:
    test_ifc_model = TEST_IFC_FILE
    test_ifc_entity = test_ifc_model.by_type("IfcWall")[0]
    test_graph = initialize_graph()
    add_entity_global_id_and_label_info_to_graph(test_ifc_entity, test_graph)
    expected_graph_str = """
        @prefix core: <https://w3id.org/digitalconstruction/core#> .
        @prefix inst: <https://w3id.org/digitalconstruction/instance#> .

        inst:0mhevRo9r5X8JNSuTZNOZH core:hasGlobalID "0mhevRo9r5X8JNSuTZNOZH" ;
            core:hasLabel "Basic Wall:Exterior_Wall - 101.6mm Brick + 203.2mm Concrete + 12.7mm Gypsum Plaster:261564" .
        """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)


def test_should_return_graph_with_units_data_when_ifc_file_is_inputted() -> None:
    pass
