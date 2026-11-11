from pathlib import Path
import hashlib
import json
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile
from PIL import Image

root = Path('/Users/jjacks20/jjacks/Conversational-AI')
scratch = root / 'tmp/slides/compass-bsc-roadmap-reconciled'
artifact = root / 'outputs/01a1b226-71b1-7090-817e-da53a9413d41/source-reconciled/output.pptx'
ns = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main', 'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
checks = {}
with zipfile.ZipFile(artifact) as z:
    assert z.testzip() is None
    names = set(z.namelist())
    slides = sorted(n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
    notes = sorted(n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n))
    assert len(slides) == len(notes) == 6
    trees = [ET.fromstring(z.read(n)) for n in slides]
    slide_text = ['\n'.join(t.itertext()) for t in trees]
    notes_text = ['\n'.join(ET.fromstring(z.read(n)).itertext()) for n in notes]
    tables = sum(len(t.findall('.//a:tbl', ns)) for t in trees)
    assert tables == 5
    for t in trees:
        assert len(t.findall('.//p:pic', ns)) == 1
    size = ET.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz', ns)
    assert (size.attrib['cx'], size.attrib['cy']) == ('12192000','6858000')
    fonts = {e.attrib['typeface'] for t in trees for e in t.findall('.//a:latin', ns)}
    assert fonts == {'Geist','Geist Light'}, fonts
    assert all('Compass + ShieldAdvisor.md' in n and 'Compass-Executive-Briefing.pdf' in n for n in notes_text)
    assert all('GAI-174' in n and 'GAI-663' in n for n in notes_text)
    assert 'One authenticated inbound journey' in slide_text[0]
    assert all(s in slide_text[1] for s in ['Atlas context', 'approved route class', 'Genesys', 'late results', 'SDK / adapter or direct API'])
    assert all(s in slide_text[2] for s in ['GAI-174', 'GAI-663', 'Separate voice/audio scope', 'Proposed extension', 'Q1', 'Q2', 'Q3', 'CSR review'])
    for i in [3,5]:
        assert all(s in slide_text[i] for s in ['Feb 1–28, 2027', 'Mar–Apr pilot / May–Jun production', 'Schedule conflict', 'Top 20', 'Q3 2027', 'Q4 2027', 'Outbound'])
    assert all(s in slide_text[4] for s in ['Added wait', 'Cost per eligible interaction', 'CCaaS + AI cost per resolved contact', 'Savings remain a hypothesis'])
    assert not any(s in '\n'.join(slide_text) for s in ['Click to add', 'TODO', 'TBD', 'Lorem ipsum'])
    rels = 0
    for n in names:
        if not n.endswith('.rels'):
            continue
        base = posixpath.dirname(posixpath.dirname(n))
        for rel in ET.fromstring(z.read(n)):
            if rel.attrib.get('TargetMode') == 'External':
                continue
            target = rel.attrib['Target']
            resolved = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(base,target))
            assert resolved in names, (n,target,resolved)
            rels += 1
    checks.update(slides=6,notes=6,nativeTables=tables,slideSize='1280x720',fonts=sorted(fonts),relationshipTargets=rels,content='PASS',sourceNotes='PASS',zipIntegrity='PASS')

records = json.loads((scratch/'editable-text-records.json').read_text())
for record in records:
    b = record['bbox']
    assert b['left'] >= 0 and b['top'] >= 0
    assert b['left'] + b['width'] <= 1280 and b['top'] + b['height'] <= 720
    assert record['textChars'] > 0
for i in range(1,7):
    with Image.open(scratch/f'preview/exported-{i:02}.png') as im:
        assert im.size == (1280,720)
checks['editableRecords'] = len(records)
checks['exportedRenders'] = 6
checks['sourceHashes'] = {
    n: hashlib.sha256((root/'Minerva/Background'/n).read_bytes()).hexdigest()
    for n in ['Compass + ShieldAdvisor.md','Compass-Executive-Briefing.pdf','GAI-174.doc','GAI-663.doc']
}
checks['outputSha256'] = hashlib.sha256(artifact.read_bytes()).hexdigest()
checks['visualReview'] = 'PENDING'
(scratch/'structural-verification.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
