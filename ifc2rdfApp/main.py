import logging
import os.path
import traceback
from pathlib import Path

import flet as ft
from icecream import ic

from ifc2rdftool.ifc2rdf_tool import create_rdf_graph_from_ifc


def main(page: ft.Page):
    def generate_rdf_file(e):
        ifc_file = ifc_file_path.value
        ic(ifc_file)
        ic(rdf_dir_path.value)
        if os.path.isfile(ifc_file) and os.path.isdir(rdf_dir_path.value):
            rdf_path = os.path.join(rdf_dir_path.value, f"{str(ifc_file_name.value).split('.')[0]}.ttl")
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
                traceback.print_exc()
            else:
                ic("RDF Graph generation is successful")
        else:
            ic(f"Either {rdf_dir_path.value} is not a valid directory or {ifc_file} is not a valid file")

    def pick_ifc_files(e: ft.FilePickerResultEvent):
        if e.files:
            ifc_file_name.value = e.files[0].name
            ifc_file_path.value = e.files[0].path
            ifc_file_name.update()
            ifc_file_path.update()
        else:
            "File is not loaded successfully"

    pick_ifc_dialog = ft.FilePicker(on_result=pick_ifc_files)
    ifc_file_name = ft.Text()
    ifc_file_path = ft.Text()
    page.overlay.append(pick_ifc_dialog)

    def pick_rdf_file_dir(e: ft.FilePickerResultEvent):
        if e.path:
            rdf_dir_path.value = e.path
            rdf_dir_path.update()
        else:
            "Folder is not loaded successfully"

    pick_rdf_file_dir_dialog = ft.FilePicker(on_result=pick_rdf_file_dir)
    rdf_dir_path = ft.Text()
    page.overlay.append(pick_rdf_file_dir_dialog)

    page.title = "IFC2RDF_TOOL"
    page_heading = ft.Text(value="IFC2RDF_TOOL", color="blue", scale=5)
    generate_rdf_button = ft.ElevatedButton("Get_RDF", on_click=generate_rdf_file, icon=ft.icons.BUILD)
    page_width = 800

    page.add(ft.Container(
        content=ft.Row(
            controls=[page_heading],
            alignment="center"
        ),
        padding=20,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.GREEN_50,
        width=page_width,
        height=100,
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
            padding=20,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_50,
            width=page_width,
            height=400,
            border_radius=10,
        )

    )


ft.app(target=main)

# import flet as ft


# def main(page: ft.Page):
#     def pick_files_result(e: ft.FilePickerResultEvent):
#         selected_files.value = (
#             ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
#         )
#         selected_files.update()
#
#     pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
#     selected_files = ft.Text()
#
#     page.overlay.append(pick_files_dialog)
#
#     page.add(
#         ft.Row(
#             [
#                 ft.ElevatedButton(
#                     "Pick files",
#                     icon=ft.icons.UPLOAD_FILE,
#                     on_click=lambda _: pick_files_dialog.pick_files(),
#                 ),
#                 selected_files,
#             ]
#         )
#     )


ft.app(target=main)
