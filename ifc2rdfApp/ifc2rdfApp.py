import os.path
import traceback

import flet as ft
from icecream import ic

from ifc2rdftool.ifc2rdf_tool import create_rdf_graph_from_ifc


def main(page: ft.Page):
    def generate_rdf_file(e):
        ifc_file = ifc_file_path.value
        rdf_dir = rdf_dir_path.value
        if not ifc_file:
            user_info.value = "Error: Please select IFC file for the conversion"
            user_info.update()
            breakpoint()
        if not rdf_dir:
            user_info.value = "Error: Please select RDF repo for storing the generated graph"
            user_info.update()
            breakpoint()
        if os.path.isfile(ifc_file) and os.path.isdir(rdf_dir):
            rdf_path = os.path.join(rdf_dir, f"{str(ifc_file_name.value).split('.')[0]}.ttl")
            if os.path.exists(rdf_path):
                ic("Removing existed RDF Graph")
                os.remove(rdf_path)
            try:
                ic("Start extracting data from IFC File")
                graph = create_rdf_graph_from_ifc(ifc_file)
                ic("Start creation of RDF Graph")
                graph.serialize(destination=rdf_path, format='ttl')
            except Exception as e:
                ic(f"An unexpected error occurred: {e}")
                traceback_str = traceback.format_exc()
                user_info.value = traceback_str
                user_info.update()
            else:
                user_info.value = "RDF Graph generation is successful"
                user_info.update()
        else:
            ic(f"Either {rdf_dir} is not a valid directory or {ifc_file} is not a valid file")
            user_info.value = f"Either {rdf_dir} is not a valid directory or {ifc_file} is not a valid file"
            user_info.update()

    user_info = ft.Text(color=ft.colors.AMBER)
    generate_rdf_button = ft.ElevatedButton("Get_RDF", on_click=generate_rdf_file, icon=ft.icons.BUILD)

    def pick_ifc_files(e: ft.FilePickerResultEvent):
        if e.files:
            ifc_file_name.value = e.files[0].name
            ifc_file_path.value = e.files[0].path
            ifc_file_name.update()
            ifc_file_path.update()
        else:
            "File is not loaded successfully"

    pick_ifc_dialog = ft.FilePicker(on_result=pick_ifc_files)
    ifc_file_name = ft.Text(color=ft.colors.AMBER_500)
    ifc_file_path = ft.Text(italic=True, width=800, selectable=True)
    page.overlay.append(pick_ifc_dialog)

    def pick_rdf_file_dir(e: ft.FilePickerResultEvent):
        if e.path:
            rdf_dir_path.value = e.path
            rdf_dir_path.update()
        else:
            "Folder is not loaded successfully"

    pick_rdf_file_dir_dialog = ft.FilePicker(on_result=pick_rdf_file_dir)
    rdf_dir_path = ft.Text(italic=True, width=800, selectable=True)
    page.overlay.append(pick_rdf_file_dir_dialog)

    page.title = "IFC2RDF (©Karlapudi)"
    page_heading = ft.Text(value="IFC2RDF", color=ft.colors.BLACK, scale=3)
    page_width = 800
    page.scroll = "auto"

    page.add(ft.Container(
        content=ft.Row(
            controls=[page_heading],
            alignment="center"
        ),
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.PINK_400,
        width=page_width,
        height=80,
        border_radius=10,
    ),
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        [ft.ElevatedButton(
                            "Pick IFC file",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: pick_ifc_dialog.pick_files(allowed_extensions=["ifc"]),
                            autofocus=True,
                        ),
                        ]
                    ),
                    ft.Row([
                        ifc_file_name
                    ]),
                    ft.Row([
                        ifc_file_path
                    ]),
                    ft.Row(
                        [ft.ElevatedButton(
                            "Pick RDF Folder",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: pick_rdf_file_dir_dialog.get_directory_path(),
                        ),
                        ],
                    ),
                    ft.Row([
                        rdf_dir_path
                    ]),
                    ft.Row([generate_rdf_button]),

                ],
                alignment='center'
            ),
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE,
            width=page_width,
            height=350,
            border_radius=10,
        ),
        ft.Container(
            content=ft.ListView(
                controls=[
                    user_info,
                ],
                expand=True,
                spacing=10,
                padding=10,
                auto_scroll=True,
            ),
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            width=page_width,
            height=150,
            border_radius=10,
        ),

    )


ft.app(target=main)
