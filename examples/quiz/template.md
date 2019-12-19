---
output: 
  pdf_document:
    latex_engine: pdflatex
    keep_tex: true
fontsize: 11pt
numbersections: false
geometry: margin=1in
header-includes: |
  \usepackage{fancyhdr}
  \pagestyle{fancy}
  \fancyhead[L]{MATH 1\\ Section \# {{section}}}
  \fancyhead[R]{Name: \underline{\hspace{1.5 in}}\\{{date}}}
  \usepackage{mathpazo}
  \usepackage{mdframed}
  \newmdenv[linecolor=black]{sol}
  \usepackage{comment}
  {{comment}}
---

!INCLUDE "quiz{{number}}_base_{{section}}.md"