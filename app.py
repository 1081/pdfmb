import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from pathlib import Path
import pdfmb
import platform
from time import sleep
import subprocess
from subprocess import call


def macos_settings():
    if platform.system() == "Darwin":
        font = Path("fonts/Menlo-Regular.ttf")
        font_size = 13 * 2
        scale = 0.5

    with dpg.font_registry():
        with dpg.font(font, font_size) as myfont:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range(0x370, 0x3FF)
    dpg.set_global_font_scale(scale)
    dpg.bind_font(myfont)


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")


def update_show_pdfs(sender, app_data, user_data):
    pass


def update_path_to_output():
    if not dpg.get_value("custom folder"):
        pass


def search_folder(sender, folder, user_data):
    dpg.show_item("search folder indicator")
    if folder:
        if Path(folder).is_dir():
            pdfs = sorted(Path(folder).rglob("*.pdf"))
            dpg.set_item_label("show pdfs", label=f"show PDFs ({len(pdfs)})")
            dpg.hide_item("search folder indicator")
            update_path_to_output()
            return
    dpg.set_item_label("show pdfs", label="no valid path")
    dpg.hide_item("search folder indicator")


def open_output_folder():
    targetDirectory = "~/Desktop"
    targetDirectory = ""
    call(["open", targetDirectory])
    # subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')


def show_existing_pdf(sender, app_data, user_data):
    if app_data:
        dpg.show_item("group existing pdf")
    else:
        dpg.hide_item("group existing pdf")


def custom_filename(sender, app_data, user_data):
    if app_data:
        dpg.show_item("info timestamp")
    else:
        dpg.hide_item("info timestamp")


dpg.create_context()

macos_settings()

spacer_height = 15


with dpg.window(tag="Primary Window"):
    dpg.add_text("Merge PDF files with bookmarks")
    # dpg.add_radio_button(
    #     (
    #         "Create new PDF",
    #         "Add to an existing PDF (the original file will not be modified)",
    #     ),
    #     callback=show_existing_pdf,
    #     horizontal=True,
    # )
    # dpg.add_spacer(height=spacer_height)
    dpg.add_text("")
    dpg.add_text("PDF files")
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            tag="source folder",
            hint="Path to folder",
            callback=search_folder,
        )
        dpg.add_button(
            tag="show pdfs",
            label="PDFs (0)",
            width=130,
        )
        dpg.add_loading_indicator(
            radius=1.4,
            style=1,
            color=(150, 255, 150, 255),
            tag="search folder indicator",
            show=False,
        )
    # dpg.add_spacer(height=spacer_height)
    dpg.add_text("")
    dpg.add_checkbox(
        tag="add to existing pdf",
        label="Add to an existing PDF",
        callback=show_existing_pdf,
    )

    # dpg.add_spacer(height=spacer_height)

    with dpg.group(tag="group existing pdf", show=False):
        # dpg.add_text("Existing PDF")
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="existing pdf",
                hint="Path to existing PDF",
                callback=_log,
            )
            dpg.add_button(
                label="Status ok",
                width=130,
            )

    # dpg.add_spacer(height=spacer_height)
    dpg.add_text("")

    dpg.add_text("Output")
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            tag="output folder",
            hint="Path to output folder",
            callback=_log,
        )
        dpg.add_checkbox(
            tag="custom output folder",
            label="Custom output folder",
            callback=_log,
        )
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            tag="output file name",
            hint="File name",
            callback=_log,
        )
        dpg.add_checkbox(
            tag="custom  file name",
            label="Custom file name",
            callback=custom_filename,
        )
    dpg.add_text(
        "A unique timestamp is automatically appended to the file name",
        tag="info timestamp",
        show=False,
    )
    # dpg.add_spacer(height=spacer_height)
    dpg.add_text("")

    dpg.add_checkbox(
        tag="flatten structure",
        label="Flatten folder structure in bookmark outline",
    )
    # dpg.add_spacer(height=spacer_height)
    dpg.add_text("")

    with dpg.group(horizontal=True):
        dpg.add_button(
            tag="create pdf",
            label="Create PDF",
            width=150,
            callback=_log,
        )
        dpg.add_text("PDF file created with 123 pages and 12 bookmakrs")

    dpg.add_button(
        tag="go to output file",
        label="Go to output file",
        width=150,
        callback=open_output_folder,
    )

    # demo.show_demo()

    # merge
    # pdfmb.merge_from_folder(
    #     source_folder=Path("example pdfs"),
    #     output_folder=Path("output"),
    # )

    # add
    # pdfmb.add_from_folder(
    #     source_folder=Path("example pdfs"),
    #     existing_pdf=Path("example pdfs/file1.pdf"),
    #     add_flat_hierachy=True,
    # )

dpg.create_viewport(title="pdfmb", width=900, height=550)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
