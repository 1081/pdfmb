# pdfmb
Merge PDF files with bookmarks

<p float="left">
<img height="400" alt="folders" src="docs/img/folders.png">
<img height="400" alt="outline" src="docs/img/outline.png">
</p>


## Installation
You can install this package via pip.
```
pip install pdfmb
```

## Features
- **merge** PDFs from a **list** into a **new** pdf
- **add** PDFs from a **list** to an **existing** pdf
- **merge all** PDFs from a **folder** into a **new** pdf
- **add all** PDFs from a **folder** to an **existing** pdf
- option to **conserve** or **flatten** the folder structure in the bookmark outline
- existing PDF files are **not modified**
    - the `add` and `add_from_folder` functions create a **new PDF** at the same location with a **timestamp**


## Usage
```python
from pathlib import Path
import pdfmb
```

```python
pdfmb.merge(
    pdfs_to_merge=Path("example pdfs").rglob("*.pdf"),
    output_folder=Path("output"),
)
```

```python
pdfmb.add(
    pdfs_to_add=Path("example pdfs").rglob("*.pdf"),
    existing_pdf=Path("example pdfs/file1.pdf"),
)
```

```python
pdfmb.merge_from_folder(
    source_folder=Path("example pdfs"),
    output_folder=Path("output"),
)
```

```python
pdfmb.add_from_folder(
    source_folder=Path("example pdfs"),
    existing_pdf=Path("example pdfs/file1.pdf"),
    add_flat_hierachy=True,
)
```