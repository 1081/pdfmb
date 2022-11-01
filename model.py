from dataclasses import dataclass, field
from pathlib import Path


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
            self.existing_pdf = Path(file)  # .absolute()
        else:
            self.existing_pdf = None
        return self.existing_pdf

    def set_output_folder(self, folder):
        if folder and Path(folder).is_dir():
            self.output_folder = Path(folder).absolute()
        else:
            self.output_folder = self.default_output_folder
        return self.output_folder

    def set_output_filename(self):
        if self.add and self.existing_pdf:
            return f"{self.existing_pdf.stem} - PDFs added"
        if self.add:
            return ""
        else:
            return "PDFs merged"

    @property
    def default_output_folder(self):
        if self.existing_pdf:
            output_folder = self.existing_pdf.parent
        else:
            output_folder = Path.home() / "Desktop"
        return output_folder.absolute()

    @property
    def default_output_filename(self):
        return "PDFs merged"


model = Model()
