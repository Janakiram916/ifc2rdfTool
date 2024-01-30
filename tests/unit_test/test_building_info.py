from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.building_info import add_building_info_to_graph
from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


def test_should_return_graph_with_complete_building_data_when_entity_type_is_ifc_building() -> (
    None
):
    test_graph = initialize_graph()
    test_building_entity = TEST_IFC_FILE.by_type("IfcBuilding")[0]
    add_building_info_to_graph(test_building_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        inst:04XCdhzWXDtBhVSPPuhCyX bot:hasBuilding inst:04XCdhzWXDtBhVSPPuhCyY .
        inst:04XCdhzWXDtBhVSPPuhCyY a bot:Building .
        """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
