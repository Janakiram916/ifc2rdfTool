import ifcopenshell
from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.ifc2rdf_tool import (_add_project_info_to_graph,
                                      _initialize_graph)

_TEST_IFC_FILE_PATH = "tests/test_resources/Demonstration_Model_V1_DTV_4.ifc"
_TEST_IFC_FILE = ifcopenshell.open(_TEST_IFC_FILE_PATH)


def test_should_return_graph_with_project_data_when_ifc_file_is_inputted() -> None:
    test_graph = _initialize_graph()
    _add_project_info_to_graph(_TEST_IFC_FILE, test_graph)
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
