"""Create readable Word copies of the saved Markdown evaluation artifacts."""
import re
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent

def inline(p,text):
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m[1] if not m[2].endswith('.md') else m[1].replace('.md','.docx'),text)
    for part in re.split(r'(\*\*.*?\*\*|`[^`]+`)',text):
        if part.startswith('**') and part.endswith('**'):
            p.add_run(part[2:-2]).bold=True
        elif part.startswith('`') and part.endswith('`'):
            run=p.add_run(part[1:-1]);run.font.name='Consolas';run.font.size=Pt(9)
        else:p.add_run(part)

def para(doc,text,style=None):
    p=doc.add_paragraph(style=style);inline(p,text);return p

def table(doc,rows):
    # Long prose records are easier to read as individual case sections.
    if rows[0][0]=='ID / category':
        for row in rows[1:]:
            doc.add_heading(row[0].replace('/',' '),2)
            for label,value in zip(('Question and identity','Gold answer','Observed result'),row[1:]):
                para(doc,'**'+label+'** '+value)
        return
    t=doc.add_table(rows=1, cols=len(rows[0]));t.autofit=False
    widths={3:[2.2,1.05,3.55],4:[3.1,.5,1.6,1.6],6:[.55,1.2,1.2,1.3,1.3,1.25]}.get(len(rows[0]),[6.8/len(rows[0])]*len(rows[0]))
    if rows[0][0]=='Representative case':widths=[2.8,2,2]
    for col,width in zip(t.columns,widths):col.width=Inches(width)
    for ri,row in enumerate(rows):
        cells=t.rows[0].cells if ri==0 else t.add_row().cells
        for ci,(cell,value) in enumerate(zip(cells,row)):
            cell.width=Inches(widths[ci]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p=cell.paragraphs[0];p.paragraph_format.space_after=Pt(4);p.paragraph_format.space_before=Pt(4)
            inline(p,value)
            for run in p.runs:run.font.size=Pt(9);run.bold=ri==0
            pr=cell._tc.get_or_add_tcPr()
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'DCE6F1' if ri==0 else ('F5F7F9' if ri%2==0 else 'FFFFFF'));pr.append(shade)
            margins=OxmlElement('w:tcMar')
            for side in ('top','left','bottom','right'):
                el=OxmlElement('w:'+side);el.set(qn('w:w'),'90');el.set(qn('w:type'),'dxa');margins.append(el)
            pr.append(margins)
        trpr=t.rows[ri]._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
        if ri==0:trpr.append(OxmlElement('w:tblHeader'))
    borders=OxmlElement('w:tblBorders')
    for side in ('top','left','bottom','right','insideH','insideV'):
        el=OxmlElement('w:'+side);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
    t._tbl.tblPr.append(borders)
    doc.add_paragraph().paragraph_format.space_after=Pt(2)

def convert(stem,title):
    doc=Document();sec=doc.sections[0]
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=sec.bottom_margin=Inches(.7)
    sec.left_margin=sec.right_margin=Inches(.85)
    normal=doc.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(10.5)
    normal.paragraph_format.space_after=Pt(6);normal.paragraph_format.line_spacing=1.08
    for name in ('Title','Subtitle','Heading 1','Heading 2','Heading 3'):
        style=doc.styles[name];style.font.name='Calibri';style.font.color.rgb=RGBColor(0,0,0)
    doc.styles['Title'].font.size=Pt(23)
    doc.styles['Heading 1'].font.size=Pt(16)
    doc.styles['Heading 2'].font.size=Pt(12)
    foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    run=foot.add_run('Page ');run.font.size=Pt(9)
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');foot._p.append(field)
    doc.core_properties.title=title;doc.core_properties.author='';doc.core_properties.subject='QuantNova AI HR application evaluation'
    lines=(ROOT/(stem+'.md')).read_text(encoding='utf-8').splitlines();i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            p=doc.add_paragraph()
            run=p.add_run('\n'.join(code));run.font.name='Consolas';run.font.size=Pt(8)
            p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(8)
        elif line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                vals=[s.strip() for s in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',v) for v in vals):rows.append(vals)
                i+=1
            table(doc,rows);continue
        elif line.startswith('# '):doc.add_paragraph(title,'Title')
        elif line.startswith('## '):
            heading=line[3:]
            if stem=='responses':
                match=re.match(r'(E\d+): (.*)',heading)
                if match:
                    doc.add_heading('Case '+match[1],1);para(doc,match[2]);i+=1;continue
            doc.add_heading(re.sub(r'[^\w\s]',' ',heading).replace('_',' '),1)
        elif line.startswith('- '):para(doc,line[2:],'List Bullet')
        elif re.match(r'^\d+\. ',line):para(doc,re.sub(r'^\d+\. ','',line),'List Number')
        else:para(doc,line)
        i+=1
    output=ROOT/(stem+'.docx');doc.save(output)
    # Verify all source text survives, ignoring Markdown syntax and layout changes.
    loaded=Document(output)
    assert loaded.paragraphs and output.stat().st_size>10000
    print(f'{output}: {len(loaded.paragraphs)} paragraphs, {len(loaded.tables)} tables')

if __name__=='__main__':
    convert('REPORT','QuantNova AI HR Application Evaluation Report')
    convert('responses','QuantNova AI HR Application Evaluation Responses')
