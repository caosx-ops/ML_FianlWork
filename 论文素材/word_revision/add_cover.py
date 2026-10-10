from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
root=Path.cwd();src=root/'占位学号-占位姓名-机器学习算法课程论文-规范修订版.docx';d=Document(src);orig=d.paragraphs[0]
items=[('机器学习算法',26,65,12,'黑体',True),('课程结业论文',22,0,44,'黑体',True),('PCA降维对手写数字识别性能的影响研究',18,0,44,'黑体',True),('学校名称：待填写',12,0,10,'宋体',False),('学院名称：待填写',12,0,10,'宋体',False),('专业班级：待填写',12,0,10,'宋体',False),('学生姓名：待填写',12,0,10,'宋体',False),('学生学号：待填写',12,0,10,'宋体',False),('任课教师：待填写',12,0,30,'宋体',False),('提交日期：待填写',12,0,0,'宋体',False)]
last=None
for text,size,before,after,font,bold in items:
 p=orig.insert_paragraph_before(text);last=p;p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Pt(0);p.paragraph_format.line_spacing=Pt(28 if size>=18 else 22);p.paragraph_format.space_before=Pt(before);p.paragraph_format.space_after=Pt(after);p.paragraph_format.keep_with_next=True
 r=p.runs[0];r.font.name='Times New Roman';r._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),font);r.font.size=Pt(size);r.bold=bold
last.paragraph_format.keep_with_next=False;last.add_run().add_break()
# Force the original manuscript to begin on a new page after the cover.
orig.paragraph_format.page_break_before=True
# Remove any inherited title border so the manuscript opens cleanly.
ppr=orig._p.get_or_add_pPr()
pbdr=ppr.find(qn('w:pBdr'))
if pbdr is not None: ppr.remove(pbdr)
style=orig.style._element
sppr=style.find(qn('w:pPr'))
if sppr is not None:
    spbdr=sppr.find(qn('w:pBdr'))
    if spbdr is not None: sppr.remove(spbdr)
# A first-page footer should be empty; body keeps existing footer.
d.sections[0].different_first_page_header_footer=True
# Clear first-page footer, preserving body footer page numbering.
for p in d.sections[0].first_page_footer.paragraphs:p.clear()
# Start body page number at 1 in the existing section.
sec=d.sections[0];from docx.oxml import OxmlElement
pg=sec._sectPr.find(qn('w:pgNumType'))
if pg is None:pg=OxmlElement('w:pgNumType');sec._sectPr.append(pg)
pg.set(qn('w:start'),'1')
out=root/'占位学号-占位姓名-机器学习算法课程论文-含封面版.docx';d.save(out);print(out)

