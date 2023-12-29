import ifcopenshell
from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.ifc2rdf_tool import (add_project_info_to_graph,
                                      initialize_graph)

TEST_IFC_FILE_PATH = "tests/test_resources/Demonstration_Model_V1_DTV_4.ifc"
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


def test_should_return_graph_with_units_data_when_ifc_file_is_inputted() -> None:
    pass
