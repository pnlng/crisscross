# Example: PhD Applications

I'm applying to PhD programs. The main body of my personal statement is the same for each program, except for places where I mention the name of the program. I also have an end paragraph tailored to each program. 

My desired results:

University of Michigan|University of Chicago
:---:|:---:|
![](../../screenshots/michigan.png)|![](../../screenshots/uchicago.png)

## Templates

My `template.md` looks like this:

```
I was born in Michigan.

I have published in \textit{Science}.

I am applying to {{school_alt_name}}’s PhD program because {{school}} is awesome. 

!INCLUDE "custom/{{school}}_last.md"
```

The template makes reference to my end paragraphs customized for each program, which I place under `custom/`.

```
custom/
    Michigan_last.md
    UChicago_last.md
```

The one for Michigan, `Michigan_last.md`, looks like this:

```markdown
Michigan is where home is. 
```

I also have a separate `header.md` that contains a [YAML metadata block](https://pandoc.org/MANUAL.html#extension-yaml_metadata_block), which tells pandoc how to style my PDF. It contains LaTeX commands that control the styling of the PDF, which pandoc will include in the header of an intermediary LaTeX file. 

```yaml
---
output: 
  pdf_document
fontsize: 12pt
numbersections: true
geometry: margin=1in
header-includes: |
  \usepackage{xcolor}
  \usepackage{fancyhdr}
  \pagestyle{fancy}
  \renewcommand{\headrulewidth}{0pt}
  \usepackage{setspace}
  \setstretch{1}
  \usepackage{mathpazo}
  \setlength{\parskip}{1.1em}
  \usepackage{lastpage}
  \cfoot{\color{gray}\thepage\ of \pageref{LastPage}}
---

\fancyhead[L]{\textcolor{gray}{Candidate: Jane Doe}}
\fancyhead[C]{\textcolor{gray}{Statement of Purpose}}
\fancyhead[R]{\textcolor{gray}{jane.doe@school.edu}}
```


## Variables in YAML

For each school I'm applying to, I create a YAML file under `custom`. 

```
custom/
    Michigan.yaml
    UChicago.yaml
```

Each specifies one set of values for the variables that occurs in my templates. The one for Michigan:

```yaml
school: Michigan
school_alt_name: the University of Michigan
```

## Conversion

I run the following command. 

```shell
crisscross process header.md template.md
```

By default, CrissCross will take all the YAML files under `custom/`. For each file/set of variables, it will first generate a composite Markdown file, and then through pandoc, a PDF, wherein placeholder expressions like `` are replaced as specified. 

The output files will be placed under `docs/` by default, each named after its corresponding YAML file. 

```
docs/
    Michigan.md
    Michigan.pdf
    UChicago.md
    Uchicago.pdf
```


In this example, we've only used the default settings of the `process` command. CrissCross is much more customizable than that! Check out the [main documentation](../../) for more details.
