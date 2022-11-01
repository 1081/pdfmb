from pathlib import Path
from typing import Callable, Iterable

from pikepdf import Pdf, OutlineItem
from pdfmb.utils import timestamp_outline, timestamp_file


def _append_pdfs(
    p: Pdf,
    pdfs: Iterable[Path],
    root_title: str,
    mapping: Callable[[str], str],
) -> None:

    page_count = len(p.pages)

    with p.open_outline() as outline:
        ol_root = OutlineItem(root_title, page_count)
        outline.root.append(ol_root)

        for file in pdfs:
            src = Pdf.open(file)
            pages = len(src.pages)

            if mapping is not None:
                file_name = mapping(file.name)
                print(file_name)
            else:
                file_name = file.name

            ol_file = OutlineItem(file_name, page_count)

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
    source_folder: Path,
    root_title: str,
    add_flat_hierachy: bool,
    mapping: Callable[[str], str],
) -> int:

    pdfs = sorted(source_folder.rglob("*.pdf"))

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
            f"{source_folder.name} (folder structure flattend)", page_count
        )

        if add_flat_hierachy:
            ol_root.children.append(ol_flat)

        ol_root.children.append(dirs[source_folder])

        for file in sorted(source_folder.rglob("*.pdf")):
            src = Pdf.open(file)
            pages = len(src.pages)

            if mapping is not None:
                file_name = mapping(file.name)
                print(file_name)
            else:
                file_name = file.name

            ol_file = OutlineItem(file_name, page_count)

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

    return len(pdfs)


def add(
    pdfs_to_add: Iterable[Path],
    existing_pdf: Path,
    mapping: Callable = None,
):
    """Extends an existing pdf and stores a new file at the same location"""
    p = Pdf.open(existing_pdf)
    p.add_blank_page()

    pdfs = sorted(pdfs_to_add)

    _append_pdfs(
        p,
        pdfs,
        f"PDFs added {timestamp_outline()}",
        mapping,
    )

    output_file = existing_pdf.with_stem(
        f"{existing_pdf.stem} - PDFs added {timestamp_file()}"
    )
    p.save(output_file)
    p.close()

    print(f"pdfbm: {len(pdfs)} PDFs added -> {output_file.absolute()}")


def merge(
    pdfs_to_merge: Iterable[Path],
    output_folder: Path,
    filename: str = "PDFs merged",
    mapping: Callable = None,
):
    """Merges pdfs into a new file, existing bookmarks will be overwritten"""
    p = Pdf.new()
    pdfs = sorted(pdfs_to_merge)

    _append_pdfs(
        p,
        pdfs,
        f"PDFs merged {timestamp_outline()}",
        mapping,
    )

    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f"{filename} {timestamp_file()}.pdf"
    p.save(output_file)
    p.close()

    print(f"pdfbm: {len(pdfs)} PDFs merged -> {output_file.absolute()}")


def add_from_folder(
    source_folder: Path,
    existing_pdf: Path,
    add_flat_hierachy: bool = False,
    output_folder: str = None,
    filename: str = None,
    mapping: Callable = None,
):
    """Extends an existing pfd with all pdfs from a folder and stores a new file at the same location"""
    p = Pdf.open(existing_pdf)
    p.add_blank_page()

    z = _append_pdfs_from_folder(
        p,
        source_folder,
        f"PDFs added {timestamp_outline()}",
        add_flat_hierachy,
        mapping,
    )

    if filename and output_folder:
        output_file = output_folder / f"{filename} {timestamp_file()}.pdf"
    else:
        output_file = existing_pdf.with_stem(
            f"{existing_pdf.stem} - PDFs added {timestamp_file()}"
        )
    p.save(output_file)
    p.close()

    print(f"pdfbm: {z} PDFs added -> {output_file.absolute()}")


def merge_from_folder(
    source_folder: Path,
    output_folder: Path,
    filename: str = "PDFs merged",
    add_flat_hierachy: bool = False,
    mapping: Callable = None,
):
    """Merges all pdfs from a folder into a new file, existing bookmarks will be overwritten"""
    p = Pdf.new()
    p.add_blank_page()

    z = _append_pdfs_from_folder(
        p,
        source_folder,
        f"PDFs merged {timestamp_outline()}",
        add_flat_hierachy,
        mapping,
    )

    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f"{filename} {timestamp_file()}.pdf"
    p.save(output_file)
    p.close()

    print(f"pdfbm: {z} PDFs merged -> {output_file.absolute()}")
