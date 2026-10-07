"""Synthetic, read-only PDF packet work sample; no client files or GUI imports."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'sample'
SOURCES = OUT / 'synthetic-inputs'
SOURCES.mkdir(parents=True, exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(name, size, title, subtitle, rows, child):
    path = SOURCES / name
    c = canvas.Canvas(str(path), pagesize=size)
    w, h = size
    c.setTitle(title + ' - synthetic sample')
    c.setFillColor(HexColor('#172b3b'))
    c.setFont('Helvetica-Bold', 11)
    c.drawString(48, h - 48, 'DUN4EV / DOCUMENT WORKFLOW SAMPLE')
    c.setFillColor(HexColor('#586979'))
    c.setFont('Helvetica', 9)
    c.drawString(48, h - 66, 'SYNTHETIC DEMO - NOT A CLIENT DOCUMENT')
    c.setFillColor(HexColor('#172b3b'))
    c.setFont('Helvetica-Bold', 26)
    c.drawString(48, h - 124, title)
    c.setFont('Helvetica', 11)
    c.drawString(48, h - 147, subtitle)
    c.setStrokeColor(HexColor('#cad4dc'))
    c.line(48, h - 172, w - 48, h - 172)
    y = h - 211
    for label, value in rows:
        c.setFont('Helvetica-Bold', 10)
        c.drawString(48, y, label)
        c.setFont('Helvetica', 10)
        c.drawString(225, y, value)
        y -= 40
    c.setFillColor(HexColor('#586979'))
    c.setFont('Helvetica', 9)
    c.drawString(48, 48, 'Fictional values. No live equipment, customer data or paid-client claim.')
    c.bookmarkPage('details')
    c.addOutlineEntry(child, 'details', level=0)
    c.showPage()
    c.save()
    return path


report = source('01-report.pdf', (595, 842), 'A clear PDF packet',
    'One report, two appendices, a traceable handover.', [
        ('INPUT', 'Three synthetic PDF files.'),
        ('OUTPUT', 'Combined PDF with nested bookmarks.'),
        ('PAGE VARIANTS', 'Portrait, landscape, rotation and crop.'),
        ('SOURCE HANDLING', 'Sources preserved; SHA-256 recorded.'),
        ('SCOPE', 'PDF assembly and labels, not OCR.'),
        ('SERVICE', 'Adaptation to a confirmed reporting format.'),
    ], 'Sample scope')
app_a = source('02-appendix-a.pdf', (842, 595), 'Example operations log',
    'Illustrative rows for layout checking only.', [
        ('DEMO-001', 'Planned inspection - scheduled'),
        ('DEMO-002', 'Document review - awaiting a reviewer'),
        ('DEMO-003', 'Record export - prepared sample'),
    ], 'Illustrative log')
app_b = source('03-appendix-b.pdf', (595, 842), 'Example review sheet',
    'The checklist content is fictional, not engineering guidance.', [
        ('DOCUMENT', 'DEMO-DOC-003'),
        ('REVISION', '00 - synthetic example'),
        ('ITEM 01', 'Confirm provided source and revision.'),
        ('ITEM 02', 'Review unresolved fields manually.'),
        ('ITEM 03', 'Approve the agreed output before delivery.'),
    ], 'Illustrative review')
# A deliberate rotated/cropped input makes the example an actual boundary check.
b_reader = PdfReader(app_b)
b_writer = PdfWriter()
b_writer.clone_document_from_reader(b_reader)
b_page = b_writer.pages[0]
b_page.add_transformation(Transformation().rotate(90).translate(tx=842, ty=0))
b_page.mediabox = RectangleObject([0, 0, 842, 595])
b_page.cropbox = RectangleObject([20, 20, 822, 575])
b_page.rotate(90)
with app_b.open('wb') as f:
    b_writer.write(f)

parts = [(report, 'Report'), (app_a, 'Appendix A'), (app_b, 'Appendix B')]
before = {p.name: sha(p) for p, _ in parts}
writer = PdfWriter()
offset = 0
for path, title in parts:
    reader = PdfReader(path)
    start_offset = offset
    for page in reader.pages:
        if page.rotation:
            page.transfer_rotation_to_content()
        box = page.cropbox
        overlay = BytesIO()
        c = canvas.Canvas(overlay, pagesize=(float(page.mediabox.width), float(page.mediabox.height)))
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(HexColor('#267064'))
        c.drawRightString(float(box.right) - 24, float(box.top) - 24, title + ' / SYNTHETIC')
        c.setFillColor(HexColor('#586979'))
        c.setFont('Helvetica', 8)
        c.drawRightString(float(box.right) - 24, float(box.bottom) + 24, 'Packet page ' + str(offset + 1) + ' of 3')
        c.save()
        overlay.seek(0)
        page.merge_page(PdfReader(overlay).pages[0])
        writer.add_page(page)
        offset += 1
    top = writer.add_outline_item(title, start_offset)
    for entry in reader.outline:
        if isinstance(entry, dict) and entry.get('/Title'):
            writer.add_outline_item(str(entry['/Title']), start_offset + reader.get_destination_page_number(entry), parent=top)

final = OUT / 'synthetic-report-packet.pdf'
writer.add_metadata({'/Title': 'Synthetic report packet - Dun4ev work sample', '/Author': 'Dun4ev', '/Subject': 'Synthetic PDF assembly demonstration; not a paid client result'})
with final.open('wb') as f:
    writer.write(f)
after = {p.name: sha(p) for p, _ in parts}
assert before == after, 'Source changed during assembly'
check = PdfReader(final)
assert len(check.pages) == 3
assert all(page.rotation == 0 for page in check.pages)
def outline_entries(entries):
    result = []
    for entry in entries:
        if isinstance(entry, list):
            result.extend(outline_entries(entry))
        else:
            result.append({'title': entry.title, 'page': check.get_destination_page_number(entry) + 1})
    return result
outline = outline_entries(check.outline)
assert len(outline) == 6
for i, (page, title) in enumerate(zip(check.pages, ['Report', 'Appendix A', 'Appendix B'])):
    text = page.extract_text()
    assert title + ' / SYNTHETIC' in text
    assert 'Packet page ' + str(i + 1) + ' of 3' in text
    assert 'NOT A CLIENT DOCUMENT' in text
manifest = {'synthetic': True, 'source_files_unchanged': before == after,
    'source_sha256': before, 'source_pages': [len(PdfReader(p).pages) for p, _ in parts],
    'output_pages': len(check.pages), 'output_sha256': sha(final),
    'output_rotation': [p.rotation for p in check.pages], 'bookmarks': outline,
    'stamp_text_verified': True, 'visual_review': 'pending',
    'implementation': 'Independent reportlab/pypdf sample pipeline; existing desktop GUI not executed',
    'word_conversion_tested': False, 'ocr_tested': False}
(OUT / 'verification.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'output': str(final), 'pages': len(check.pages), 'bookmarks': len(outline), 'unchanged_sources': before == after}))
