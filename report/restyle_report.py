from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

root=Path(__file__).resolve().parent
path=root/'RecipeHub_Report_Editable.docx'
d=Document(path)
source=Image.open('C:/Users/HP/AppData/Local/Temp/codex-clipboard-e0419610-4457-4258-a11d-d68d1db86f16.png')
source.crop((220,59,308,169)).save(root/'qa/university_emblem.png')
# Replace the previous cover, retaining all subsequent report content.
body=d._element.body
first_heading=next(p for p in d.paragraphs if p.text=='1 Introduction and Requirements')
for el in list(body):
 if el is first_heading._p: break
 body.remove(el)

def cover(text='',size=12,bold=False,before=0,after=0,style=None):
 p=first_heading.insert_paragraph_before(text,style)
 p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 pf=p.paragraph_format; pf.space_before=Pt(before); pf.space_after=Pt(after); pf.line_spacing=1
 for r in p.runs: r.font.size=Pt(size); r.bold=bold
 return p

p=cover(before=15,after=24)
p.add_run().add_picture(str(root/'qa/university_emblem.png'),height=Inches(1.55))
cover('Department of Electrical and Information\nEngineering',16,True,after=10)
cover('University of Ruhuna',14,True,after=39)
cover('Mini Project Report',15,True,after=7)
cover('Web Application Development',12,True,after=6)
cover('[Confirm module code EC4307 or EE4207]',11,True,after=35)
cover('RecipeHub',16,True,style='Title',after=6)
cover('Full Stack Recipe Management and Sharing Application',12,True,after=25)
cover('[Your full name] : [Your index number]',12,after=0)
cover('Submission Date : 2026/10/31',11,before=138)
breakp=cover()
breakp.add_run().add_break(__import__('docx').enum.text.WD_BREAK.PAGE)
# Keep cover free of page numbering, matching the reference.
d.sections[0].different_first_page_header_footer=True
# Apply Times New Roman to all styles, explicit runs, table text and numbering.
for st in d.styles:
 if hasattr(st,'font'):
  st.font.name='Times New Roman'
for part in [d.part, *[s.header.part for s in d.sections], *[s.footer.part for s in d.sections]]:
 for rpr in part.element.iter(qn('w:rPr')):
  rf=rpr.find(qn('w:rFonts'))
  if rf is None: rf=OxmlElement('w:rFonts'); rpr.insert(0,rf)
  for key in list(rf.attrib): del rf.attrib[key]
  for key in ['ascii','hAnsi','eastAsia','cs']: rf.set(qn('w:'+key),'Times New Roman')
for part in [d.styles.element,d.part.numbering_part.element]:
 for rf in part.iter(qn('w:rFonts')):
  for key in list(rf.attrib): del rf.attrib[key]
  for key in ['ascii','hAnsi','eastAsia','cs']: rf.set(qn('w:'+key),'Times New Roman')
d.save(path)
check=Document(path)
assert any(p.text=='University of Ruhuna' for p in check.paragraphs)
assert any(p.text=='8 Setup Conclusion and References' for p in check.paragraphs)
print('Updated cover and Times New Roman throughout:',path)
