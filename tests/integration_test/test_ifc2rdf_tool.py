import ifcopenshell.util.element
from icecream import ic

from ifc2rdftool.ifc2rdf_tool import (
    add_entity_info_to_graph, create_rdf_graph_from_ifc,
    get_all_entity_types_from_project_decomposition, initialize_graph)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE, TEST_IFC_FILE_PATH


def test_should_return_complete_graph_from_ifc_data() -> None:
    test_graph = create_rdf_graph_from_ifc(TEST_IFC_FILE_PATH)
    test_graph.serialize(
        destination="tests/test_resources/test_graph.ttl", format="turtle"
    )


def test_manual_testing() -> None:
    # pass
    test_entity = TEST_IFC_FILE.by_type("IfcSlab")[0]
    psets_and_qtos = ifcopenshell.util.element.get_psets(test_entity)
    # ic(psets_and_qtos)
    set = get_all_entity_types_from_project_decomposition(TEST_IFC_FILE)
    # ic(set)
