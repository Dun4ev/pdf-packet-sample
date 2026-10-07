# PDF packet work sample

A synthetic report with two appendices, labels, page numbers and nested bookmarks. The example includes portrait, landscape and a deliberately encoded rotated/cropped input. All source files stay unchanged during assembly; the manifest records their SHA-256 hashes.

[Open the finished three-page PDF](sample/synthetic-report-packet.pdf) · [Verification manifest](sample/verification.json)

This is an independently implemented reportlab/pypdf example. It does not run the older PDF Attachments desktop GUI and does not demonstrate Word conversion, OCR, PDF-form extraction or paid-client work. The content is fictional. It is not engineering guidance.

## Checked on this example

- Three pages in the specified order.
- Six correctly resolved top-level/nested bookmarks.
- Labels and packet page numbers on each page.
- Source hashes unchanged during assembly.
- Rotation normalized with the visible page content preserved.
- All three final pages rendered with Poppler and visually reviewed.

These checks cover the supplied synthetic files, not arbitrary customer PDFs. Signed, encrypted or malformed files need a separately approved workflow. Stamps require confirmed empty margins in the customer layout.

## Reproduce

Use Python 3.10 or newer in a separate environment:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build_sample.py
```

On Windows use `.venv\Scripts\python.exe` instead. The builder rewrites only its own `sample/` synthetic files; do not place customer documents in that folder. It performs assertions on the result. It is a work sample with fixed fixture paths, not a general customer-facing application.

## Adapt this to your reporting workflow

A scoped pilot is **US$300 gross**: one confirmed report format, up to 10 supplied PDFs and 50 pages total, agreed labels/order/bookmarks, a combined PDF, source/output manifest and handover instructions. Five working days after project acceptance and complete approved inputs. A redacted sample and clear acceptance criteria are needed before accepting the project. Larger batches and recurring operations are quoted separately.

View the [US$300 PDF packet pilot on Freelancer](https://www.freelancer.com/service/python/pdf-report-packet-assembly-and-bookmarks), or [message me with a redacted sample](https://www.freelancer.com/u/dun4ev) before ordering. No order or payment is made by visiting this repository. Platform fees and taxes are separate from the gross service price. This sample contains no confidential client materials or credentials.
