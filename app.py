import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from pathlib import Path
import pdfmb
import platform
from subprocess import call
from dataclasses import dataclass, field

# example pdfs/file1.pdf
# example pdfs


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


# ------------------------------------------------------------------------------

dpg.create_context()

# ------------------------------------------------------------------------------

macos_settings()
spacer_height = 15

# ------------------------------------------------------------------------------

primary_window = dpg.generate_uuid()
#
source_folder = dpg.generate_uuid()
source_folder_status = dpg.generate_uuid()
source_folder_search_pdfs = dpg.generate_uuid()
source_folder_show_pdfs = dpg.generate_uuid()
source_folder_loading_indicator = dpg.generate_uuid()
#
check_add = dpg.generate_uuid()
group_existing_pdf = dpg.generate_uuid()
existing_pdf = dpg.generate_uuid()
existing_pdf_status = dpg.generate_uuid()
#
output_folder = dpg.generate_uuid()
output_folder_status = dpg.generate_uuid()
#
output_filename = dpg.generate_uuid()
timestamp_info = dpg.generate_uuid()
#
check_flatten = dpg.generate_uuid()
#
create_pdf = dpg.generate_uuid()
create_pdf_feedback = dpg.generate_uuid()
create_pdf_loading_indicator = dpg.generate_uuid()
#
goto_output_folder = dpg.generate_uuid()
open_pdf = dpg.generate_uuid()

# ------------------------------------------------------------------------------


@dataclass
class Model:
    source_folder: Path = None
    pdfs: list[int] = field(default_factory=list)
    add: bool = False
    existing_pdf: Path = None
    output_folder: Path = None
    output_filenname: str = None
    flatten: bool = False

    def set_source_folder(self, folder):
        if folder and Path(folder).is_dir():
            self.source_folder = Path(folder)
        else:
            self.source_folder = None
        return self.source_folder

    def find_pdfs(self):
        if self.source_folder:
            self.pdfs = sorted(self.source_folder.rglob("*.pdf"))
        else:
            self.pdfs = []
        return self.pdfs

    def set_existing_pdf(self, file: str):
        if file and Path(file).is_file() and file.endswith(".pdf"):
            self.existing_pdf = Path(file).absolute()
        else:
            self.existing_pdf = False
        return self.existing_pdf

    def set_output_folder(self, folder):
        if folder and Path(folder).is_dir():
            self.output_folder = Path(folder).absolute()
        else:
            self.output_folder = self.default_output_folder
        return self.output_folder

    def set_output_filename(self):
        if self.add and self.existing_pdf:
            return "added"
            # return self.existing_pdf.with_stem(f"{existing_pdf.stem} - PDFs added")
        else:
            return "PDFs merged"

    @property
    def default_output_folder(self):
        desktop = Path.home() / "Desktop"
        return desktop.absolute()

    @property
    def default_output_filename(self):
        return "PDFs merged"


def x():
    print(model)


model = Model()

# -------------------------------------------------------------------------------


def changed_source_folder(sender, folder, user_data):
    model.source_folder = []
    model.pdfs = []
    if model.set_source_folder(folder):
        dpg.set_value(source_folder_status, "ok")
        dpg.show_item(source_folder_search_pdfs)
        dpg.set_item_label(source_folder_search_pdfs, label="search ")
        dpg.hide_item(source_folder_show_pdfs)
    else:
        dpg.set_value(source_folder_status, "no valid path")
        dpg.hide_item(source_folder_search_pdfs)
        dpg.hide_item(source_folder_show_pdfs)


def clicked_source_folder_search_pdfs(sender, app_data, user_data):
    dpg.show_item(source_folder_loading_indicator)

    pdfs = model.find_pdfs()
    if pdfs:
        dpg.set_item_label(source_folder_search_pdfs, label=f"PDFs ({len(pdfs)})")
        dpg.show_item(source_folder_show_pdfs)
    else:
        # dpg.set_item_label(source_folder_show_pdfs, label="no valid path")
        dpg.hide_item(source_folder_show_pdfs)

    dpg.hide_item(source_folder_loading_indicator)


def clicked_source_show_pdfs():
    # TODO popup window
    for p in model.pdfs:
        print(p)


def update_check_add(sender, checked, user_data):
    if checked:
        model.add = True
        dpg.show_item(group_existing_pdf)

    else:
        model.add = False
        dpg.hide_item(group_existing_pdf)
    dpg.set_value(output_filename, value=model.set_output_filename())


def changed_existing_pdf(sender, file, user_data):
    if model.set_existing_pdf(file):
        dpg.set_item_label(existing_pdf_status, label="ok")
    else:
        dpg.set_item_label(existing_pdf_status, label="not found")
    dpg.set_value(output_filename, value=model.set_output_filename())


def changed_output_folder(sender, folder, user_data):
    if model.set_output_folder(folder):
        # dpg.set_item_label(output_folder_status, label="ok")
        dpg.set_value(output_folder_status, "ok")
    else:
        # dpg.set_item_label(output_folder_status, label="not found")
        dpg.set_value(output_folder_status, "not found")


def changed_output_filename(sender, filename, user_data):
    pass


def clicked_create_pdf():
    pass
    # pdfmb.merge_from_folder(
    #     source_folder=Path("example pdfs"),
    #     output_folder=Path("output"),
    # )

    # pdfmb.add_from_folder(
    #     source_folder=Path("example pdfs"),
    #     existing_pdf=Path("example pdfs/file1.pdf"),
    #     add_flat_hierachy=True,
    # )


def clicked_goto_output_folder():
    call(["open", model.output_folder.absolute()])


def clicked_open_pdf():
    pass


def clicked_debug():
    print("")
    print(model)
    print("")


# ------------------------------------------------------------------------------

with dpg.window(tag=primary_window):
    dpg.add_text("Merge PDF files with bookmarks")
    dpg.add_text("")

    # ------------------------------------------------------------------------------

    dpg.add_text("PDF files")
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            tag=source_folder,
            hint="Path to folder",
            callback=changed_source_folder,
        )
        dpg.add_text(
            tag=source_folder_status,
            default_value="no valid path",
        )
        dpg.add_button(
            tag=source_folder_search_pdfs,
            label="search for pdfs",
            width=130,
            show=False,
            callback=clicked_source_folder_search_pdfs,
        )
        dpg.add_button(
            tag=source_folder_show_pdfs,
            label="show pdfs",
            width=130,
            show=False,
            callback=clicked_source_show_pdfs,
        )
        dpg.add_loading_indicator(
            tag=source_folder_loading_indicator,
            radius=1.4,
            style=1,
            color=(150, 255, 150, 255),
            show=False,
        )
    dpg.add_text("")

    # ------------------------------------------------------------------------------

    dpg.add_checkbox(
        tag=check_add,
        label="Add to existing PDF",
        callback=update_check_add,
    )
    with dpg.group(tag=group_existing_pdf, show=False):
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag=existing_pdf,
                hint="Path to existing PDF",
                callback=changed_existing_pdf,
            )
            dpg.add_button(
                tag=existing_pdf_status,
                label="no valid path",
                width=100,
                enabled=False,
            )
    dpg.add_text("")

    # ------------------------------------------------------------------------------

    dpg.add_text("Output")
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            tag=output_folder,
            default_value=model.default_output_folder,
            hint="Path to output folder",
            callback=changed_output_folder,
        )
        dpg.add_text(
            "",
            tag=output_folder_status,
        )
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            tag=output_filename,
            hint="File name",
            default_value=model.default_output_filename,
            callback=changed_output_filename,
        )
        dpg.add_text("- YYYY-MM-DD HHMMSS.pdf")

    dpg.add_text(
        "A unique timestamp is automatically appended to the file name",
        tag=timestamp_info,
        show=False,
        color=(130, 130, 130),
    )
    dpg.add_text("")

    # ------------------------------------------------------------------------------

    dpg.add_checkbox(
        tag=check_flatten,
        label="Flatten folder structure in bookmark outline",
    )
    dpg.add_text("")

    # ------------------------------------------------------------------------------

    with dpg.group(horizontal=True):
        dpg.add_button(
            tag=create_pdf,
            label="Create PDF",
            width=150,
            callback=clicked_create_pdf,
        )
        dpg.add_text(
            "PDF file created with 123 pages and 12 bookmakrs",
            tag=create_pdf_feedback,
        )

    dpg.add_text("")
    dpg.add_button(
        tag=goto_output_folder,
        label="Open output",
        width=150,
        callback=clicked_goto_output_folder,
    )
    dpg.add_button(
        tag=open_pdf,
        label="Open PDF",
        width=150,
        callback=clicked_open_pdf,
    )

    # ------------------------------------------------------------------------------

    dpg.add_text("")
    dpg.add_button(
        tag="debug",
        label="debug",
        width=300,
        callback=clicked_debug,
    )

    # demo.show_demo()


dpg.create_viewport(title="pdfmb", width=900, height=550)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(primary_window, True)
dpg.start_dearpygui()
dpg.destroy_context()
