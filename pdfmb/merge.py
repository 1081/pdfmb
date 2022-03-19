from pathlib import Path
from typing import Iterable

from pikepdf import Pdf, OutlineItem
from pdfmb.utils import timestamp_outline, timestamp_file


def _append_pdfs(
    p: Pdf,
    pdfs: Iterable[Path],
    root_title: str,
) -> None:

    page_count = len(p.pages)

    with p.open_outline() as outline:
        ol_root = OutlineItem(root_title, page_count)
        outline.root.append(ol_root)

        for file in pdfs:
            src = Pdf.open(file)
            pages = len(src.pages)

            ol_file = OutlineItem(file.name, page_count)
            ol_root.children.append(ol_file)

            if pages > 1:
                for page in range(pages):
                    ol_file.children.append(
                        OutlineItem(f"Page {page+1}", page_count + page)
                    )

            page_count += pages
            p.pages.extend(src.pages)


def _append_pdfs_from_folder(
    p: Pdf,
    sorce_folder: Path,
    root_title: str,
    add_flat_hierachy: bool,
) -> None:

    pdfs = sorted(sorce_folder.rglob("*.pdf"))

    dirs = {}
    for pdf in pdfs:
        for d in pdf.parents:
            if d not in dirs and str(d) != str("."):
                dirs[d] = OutlineItem(d.name, 0)

    page_count = len(p.pages)

    # NOTE add folder hierachy -> order in outline, folders before files
    # for d in dirs:
    #     if d.parent in dirs:
    #         dirs[d.parent].children.append(dirs[d])

    with p.open_outline() as outline:
        ol_root = OutlineItem(root_title, page_count)
        outline.root.append(ol_root)

        ol_flat = OutlineItem(
            f"{sorce_folder.name} (folder structure flattend)", page_count
        )

        if add_flat_hierachy:
            ol_root.children.append(ol_flat)

        ol_root.children.append(dirs[sorce_folder])

        for file in sorted(sorce_folder.rglob("*.pdf")):
            src = Pdf.open(file)
            pages = len(src.pages)

            ol_file = OutlineItem(file.name, page_count)

            # add flat_hierachy
            ol_flat.children.append(ol_file)

            # add folder hierachy
            dirs[file.parent].children.append(ol_file)

            if pages > 1:
                for page in range(pages):
                    ol_file.children.append(
                        OutlineItem(f"Page {page+1}", page_count + page)
                    )

            page_count += pages
            p.pages.extend(src.pages)

        # NOTE add folder hierachy -> order in outline, files before folders
        for d in dirs:
            if d.parent in dirs:
                dirs[d.parent].children.append(dirs[d])


def add(
    pdfs_to_add: Iterable[Path],
    existing_pdf: Path,
):
    """Extends an existing pdf and stores a new file at the same location"""
    p = Pdf.open(existing_pdf)
    p.add_blank_page()

    _append_pdfs(
        p,
        sorted(pdfs_to_add),
        f"PDFs added {timestamp_outline()}",
    )

    p.save(
        existing_pdf.with_stem(f"{existing_pdf.stem} - PDFs added {timestamp_file()}")
    )
    p.close


def merge(
    pdfs_to_merge: Iterable[Path],
    output_folder: Path,
    filename: str = "PDFs merged",
):
    """Merges pdfs into a new file, existing bookmarks will be overwritten"""
    p = Pdf.new()

    _append_pdfs(
        p,
        sorted(pdfs_to_merge),
        f"PDFs merged {timestamp_outline()}",
    )

    output_folder.mkdir(parents=True, exist_ok=True)
    p.save(output_folder / f"{filename} {timestamp_file()}.pdf")
    p.close


def add_from_folder(
    source_folder: Path,
    existing_pdf: Path,
    add_flat_hierachy: bool = False,
):
    """Extends an existing pfd with all pdfs from a folder and stores a new file at the same location"""
    p = Pdf.open(existing_pdf)
    p.add_blank_page()

    _append_pdfs_from_folder(
        p,
        source_folder,
        f"PDFs added {timestamp_outline()}",
        add_flat_hierachy,
    )

    p.save(
        existing_pdf.with_stem(f"{existing_pdf.stem} - PDFs added {timestamp_file()}")
    )
    p.close


def merge_from_folder(
    source_folder: Path,
    output_folder: Path,
    filename: str = "PDFs merged",
    add_flat_hierachy: bool = False,
):
    """Merges all pdfs from a folder into a new file, existing bookmarks will be overwritten"""
    p = Pdf.new()
    p.add_blank_page()

    _append_pdfs_from_folder(
        p,
        source_folder,
        f"PDFs merged {timestamp_outline()}",
        add_flat_hierachy,
    )

    output_folder.mkdir(parents=True, exist_ok=True)
    p.save(output_folder / f"{filename} {timestamp_file()}.pdf")
    p.close
