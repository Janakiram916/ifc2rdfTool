import ifcopenshell
from icecream import ic
from rdflib import Graph



def extract_project_info(file: str):
    ifc_model = ifcopenshell.open(file)
    project = ifc_model.by_type('IfcProject')
    ic(project[0].get_info())
    ic(project[0].UnitsInContext.get_info())


def extract_units_info(file: str):
    ifc_model = ifcopenshell.open(file)
    units = ifc_model.by_type('IfcUnitAssignment')
    ic(units[0].get_info())

if __name__ == '__main__':
    pass
