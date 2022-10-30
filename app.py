import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from pathlib import Path
import pdfmb
import platform
from time import sleep


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


def search_folder(sender, folder, user_data):
    dpg.show_item("search folder indicator")
    if folder:
        if Path(folder).is_dir():
            pdfs = sorted(Path(folder).rglob("*.pdf"))
            dpg.set_item_label("show pdfs", label=f"show PDFs ({len(pdfs)})")
            dpg.hide_item("search folder indicator")
            return
    dpg.set_item_label("show pdfs", label="no valid path")
    dpg.hide_item("search folder indicator")


dpg.create_context()

macos_settings()

spacer_height = 20

with dpg.window(tag="Primary Window"):
    dpg.add_text("Merge PDF files with bookmarks")
    dpg.add_radio_button(
        ("Create new PDF", "Add to existing PDF"), callback=_log, horizontal=True
    )
    dpg.add_spacer(height=spacer_height)

    dpg.add_text("PDFs to be merged")
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            hint="Path to source folder",
            callback=search_folder,
            tag="source folder",
        )
        dpg.add_button(label="PDFs (0)", width=130, tag="show pdfs")
        with dpg.group():
            dpg.add_loading_indicator(
                radius=1.4,
                style=1,
                color=(150, 255, 150, 255),
                tag="search folder indicator",
                show=False,
            )

    dpg.add_spacer(height=spacer_height)

    dpg.add_text("Existing PDF")
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint="Path to existing PDF", callback=_log)
        dpg.add_button(label="status ok", width=130)

    dpg.add_spacer(height=spacer_height)

    dpg.add_text("Output")
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint="Path to output folder", callback=_log)
        dpg.add_checkbox(label="Custom folder", callback=_log)
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint="file name", callback=_log)
        dpg.add_checkbox(label="Custom filename", callback=_log)

    dpg.add_spacer(height=spacer_height)

    dpg.add_button(label="Create PDF", width=150)

    demo.show_demo()

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

dpg.create_viewport(title="pdfmb", width=900, height=350)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
