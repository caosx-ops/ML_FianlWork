# LaTeX 论文版本

`机器学习算法课程论文.tex` 是根据 `Latex模板` 中的 `HustGSClassPaper.cls` 模板，将现有 Word 论文内容迁移后的版本。

## 文件

- `机器学习算法课程论文.tex`：论文主文件，含封面、摘要、目录、正文、公式、图表和参考文献引用。
- `Bibs/mybib.bib`：5 条参考文献。
- `Figures/`：论文中使用的实验图和流程图素材。
- `HustGSClassPaper.cls`、`gbt7714-2005.bst`、`gbt7714-2015.bst`：模板依赖文件。

## 编译

请使用 XeLaTeX 编译，建议连续编译两次，并运行 BibTeX 处理参考文献：

```bash
xelatex 机器学习算法课程论文.tex
bibtex 机器学习算法课程论文
xelatex 机器学习算法课程论文.tex
xelatex 机器学习算法课程论文.tex
```

封面中的专业班级、指导教师和院系仍为“待填写”，可直接在 `.tex` 文件顶部的 `\\classnum`、`\\instructor` 和 `\\school` 中修改。
