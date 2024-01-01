import flet as ft
from icecream import ic

from ifc2rdftool.ifc2rdf_tool import create_rdf_graph_from_ifc


def main(page: ft.Page):

    def generate_rdf_file(e):
        print(file_input.value)

        graph = create_rdf_graph_from_ifc(str(file_input.value))
        graph.serialize(destination="tests/test_resources/test_graph2.ttl", format='ttl')

    page.title = "IFC2RDF_TOOL"
    page_heading = ft.Text(value="IFC2RDF_TOOL", color="blue")
    file_input = ft.TextField(hint_text="please paste ifc file path", label="IFC_FILE", border_radius=10)
    file_output = ft.TextField(hint_text="Your file is processing", label="IFC_OUTPUT", border_radius=10)
    file_load_button = ft.ElevatedButton("Load File", on_click=generate_rdf_file)
    page_width = 500
    page.add(
        ft.Card(
            content= ft.Container(
                content=ft.Row(
                    controls=[page_heading],
                    alignment="center"
                ),
                padding=20,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.AMBER_50,
                width=page_width,
                height=100,
                border_radius=10,
            ),
        ),
        ft.Container(
            content=ft.Column(
                controls=[ft.Row([file_input, file_load_button]), ft.Row([file_output])],
                alignment='center'
            ),
            padding=20,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_50,
            width=page_width,
            height=400,
            border_radius=10,
        )

    )


ft.app(target=main)
