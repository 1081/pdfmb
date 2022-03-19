# pdfmb
Merge PDF files with bookmarks

## Installation
You can install this package via pip.
```
pip install pdfmb
```

## Usage
```python
pdfmb.merge(
    pdfs_to_merge=Path("example pdfs").rglob("*.pdf"),
    output_folder=Path("output"),
)
```

```python
pdfmb.add(
    pdfs_to_add=Path("example pdfs").rglob("*.pdf"),
    existing_pdf=Path("example pdfs/root1.pdf"),
)
```

```python
pdfmb.merge_from_folder(
    source_folder=Path("example pdfs"),
    output_folder=Path("output"),
    add_flat_hierachy=True,
)
```

```python
pdfmb.add_from_folder(
    source_folder=Path("example pdfs"),
    existing_pdf=Path("example pdfs/root1.pdf"),
    add_flat_hierachy=True,
)

```