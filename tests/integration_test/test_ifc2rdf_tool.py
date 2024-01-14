from ifc2rdftool.ifc2rdf_tool import create_rdf_graph_from_ifc
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE_PATH


def test_should_return_complete_graph_from_ifc_data() -> None:
    test_graph = create_rdf_graph_from_ifc(TEST_IFC_FILE_PATH)
    test_graph.serialize(
        destination="tests/integration_test/test_resources/rdf_graphs/test_graph.ttl",
        format="turtle",
    )
