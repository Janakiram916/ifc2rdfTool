# from unittest import mock
#
# from icecream import ic
# from rdflib import Graph
# from rdflib.compare import isomorphic
#
# from ifc2rdftool.ifc2rdf_tool import initialize_graph
# from ifc2rdftool.wall_info import add_wall_info_to_graph
# from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE



# @mock.patch("ifc2rdftool.wall_info.get_valid_guid", side_effect=[
#         "2rvVZuy3X0l9ATwV2NTibB",
#         "2rvVZuy3X0l9ATwV2NTibB",
#         "2rvVZuy3X0l9ATwV2NTYSe",
#         "2rvVZuy3X0l9ATwUENTYSe",
#     ])
# @mock.patch(
#     "ifc2rdftool.wall_info.get_multiple_guids",
#     return_value=[
#         "1a8Aef4WT5O95P1duyJUJM",
#         "1JiIoLE5XAvx1zVHUdIyGn",
#         "213gwkWvf7bv0837WjMTfN",
#     ],
# )
# def test_should_return_graph_with_complete_wall_data_when_entity_type_is_ifc_wall(
#     mocked_layers_guid, mocker_layer_set_guid
# ) -> None:
#     test_graph = initialize_graph()
#     test_wall_entity = TEST_IFC_FILE.by_type("IfcWall")[0]
#     add_wall_info_to_graph(test_wall_entity, test_graph)
#     test_graph.serialize(
#         destination="tests/test_resources/test_wall_graph.ttl", format="turtle"
#     )
#     expected_graph = Graph().parse(
#         source="tests/test_resources/test_wall_graph.ttl", format="turtle"
#     )
    # assert isomorphic(test_graph, expected_graph)
