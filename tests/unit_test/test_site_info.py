from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdftool.graph_resources import PREFIXES
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from ifc2rdftool.site_info import (add_site_info_to_graph,
                                   tuple_to_decimal_latitude_or_longitude)
from tests.unit_test.test_ifc2rdf_tool import TEST_IFC_FILE


def test_should_return_longitude_decimal_when_longitude_tuple_inputted():
    test_latitude = (13, 43, 19, 0)
    expected_latitude = 13.721944444444444
    actual_latitude = tuple_to_decimal_latitude_or_longitude(test_latitude)
    assert actual_latitude == expected_latitude


def test_should_return_graph_with_site_data_when_entity_type_is_ifc_site() -> None:
    test_graph = initialize_graph()
    test_project_entity = TEST_IFC_FILE.by_type("IfcSite")[0]
    add_site_info_to_graph(test_project_entity, test_graph)
    expected_graph_str = f"""
        {PREFIXES}
        inst:04XCdhzWXDtBhVSPPuhCyZ core:hasSite inst:04XCdhzWXDtBhVSPPuhCyX .
        inst:04XCdhzWXDtBhVSPPuhCyX a bot:Site ;
            geo:lat "51.034439086666666"^^xsd:float ;
            geo:long "13.72202587111111"^^xsd:float .
        """
    expected_graph = Graph().parse(data=expected_graph_str, format="turtle")
    assert isomorphic(test_graph, expected_graph)
