from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Model:
    source_folder: Path = None
    pdfs: list[int] = field(default_factory=list)

    add: bool = False
    existing_pdf: Path = None

    custom_output_folder: bool = True
    custom_output_folder_path: Path = None

    custom_output_filename: bool = True
    custom_output_filename_str: str = ""

    flatten: bool = False

    def set_source_folder(self, folder):
        if folder and Path(folder).is_dir():
            self.source_folder = Path(folder)
        else:
            self.source_folder = False
        return self.source_folder

    def find_pdfs(self):
        if self.source_folder:
            self.pdfs = sorted(self.source_folder.rglob("*.pdf"))
        else:
            self.pdfs = []
        return self.pdfs

    def reset_pdfs(self):
        self.pdfs = []

    def set_existing_pdf(self, file: str):
        if file and Path(file).is_file() and file.endswith(".pdf"):
            self.existing_pdf = Path(file)
        else:
            self.existing_pdf = None
        return self.existing_pdf

    def set_custom_output_folder(self, folder):
        if folder and Path(folder).is_dir():
            self.custom_output_folder_path = Path(folder)
        else:
            self.custom_output_folder_path = ""
        return self.custom_output_folder_path

    def set_custom_output_filename(self, filename):
        if filename:
            self.custom_output_filename_str = filename
        else:
            self.custom_output_filename_str = ""

    @property
    def output_folder(self):
        if self.add:
            if self.custom_output_folder:
                if self.custom_output_folder_path:
                    return self.custom_output_folder_path
            if self.existing_pdf:
                return self.existing_pdf.parent
        else:
            if self.custom_output_folder:
                if self.custom_output_folder_path:
                    return self.custom_output_folder_path
                else:
                    desktop = Path.home() / "Desktop"
                    if desktop.is_dir():
                        return desktop
                    else:
                        return Path.home()
            else:
                desktop = Path.home() / "Desktop"
                if desktop.is_dir():
                    return desktop
                else:
                    return Path.home()

    @property
    def output_filename(self):
        if self.add:
            if self.existing_pdf:
                return f"{self.existing_pdf.stem} - PDFs added"
            if self.add:
                return ""
        else:
            if self.custom_output_filename:
                if self.custom_output_filename_str:
                    return self.custom_output_filename_str
                else:
                    return "PDFs merged"
            else:
                return "PDFs merged"


model = Model()
