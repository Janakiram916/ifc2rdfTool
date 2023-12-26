from ifc2rdftool.ifc2rdf_tool import extract_project_info, extract_units_info


def test_should_extract_project_data_when_ifc_file_is_inputted() -> None:
    test_ifc_file_path = "tests/test_resources/Demonstration_Model_V1_DTV_4.ifc"
    extract_project_info(test_ifc_file_path)
