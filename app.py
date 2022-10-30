import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from pathlib import Path
import pdfmb

dpg.create_context()

with dpg.window(tag="Primary Window"):

    def _log(sender, app_data, user_data):
        print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

    with dpg.group(horizontal=True):
        dpg.add_text("Select source folder with pdfs:")
        dpg.add_text("pfad ok, 123 pdfs found")
        dpg.add_button(label="show list of pdfs")
    dpg.add_input_text(label="source path", hint="path", callback=_log)

    dpg.add_text("Select mode:")
    dpg.add_radio_button(
        ("merge from folder", "add from folder"), callback=_log, horizontal=True
    )
    dpg.add_input_text(label="filename", hint="filename", callback=_log)

    demo.show_demo()

    dpg.add_text("§", label="path")

    # merge
    pdfmb.merge_from_folder(
        source_folder=Path("example pdfs"),
        output_folder=Path("output"),
    )

    # add
    # pdfmb.add_from_folder(
    #     source_folder=Path("example pdfs"),
    #     existing_pdf=Path("example pdfs/file1.pdf"),
    #     add_flat_hierachy=True,
    # )

dpg.create_viewport(title="Merge PDF files with bookmarks", width=1000, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
