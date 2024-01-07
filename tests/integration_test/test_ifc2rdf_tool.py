import ifcopenshell.util.element

from ifc2rdftool.ifc2rdf_tool import (add_entity_info_to_graph,
                                      create_rdf_graph_from_ifc,
                                      initialize_graph)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE, TEST_IFC_FILE_PATH


def test_should_return_complete_graph_from_ifc_data() -> None:
    test_graph = create_rdf_graph_from_ifc(TEST_IFC_FILE_PATH)
    test_graph.serialize(
        destination="tests/test_resources/test_graph.ttl", format="turtle"
    )


def test_manual_testing() -> None:
    pass
    # test_entity = TEST_IFC_FILE.by_type("IfcSlab")
    # for item in test_entity:
    # ic(item.get_info())
    # layer_set_usage = ifcopenshell.util.element.get_material(item)
    # ic(layer_set_usage)
    # ic(layer_set_usage.get_info())
    # if layer_set_usage.get_info()['type'] == 'IfcMaterialLayerSetUsage':
    #     ic(layer_set_usage.ForLayerSet.get_info())
