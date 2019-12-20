![](https://img.shields.io/pypi/pyversions/crisscross)

# CrissCross

CrissCross is a Markdown-centric templating engine. 

Some of its features: 

- Replace Mustache-style placeholders
- Include/import subfiles `!INCLUDE "subfile.md"`
- Convert to other formats using [pandoc](https://pandoc.org/) or [rmarkdown](https://github.com/rstudio/rmarkdown)

<details>

<summary>Table of Contents</summary>

- [CrissCross](#crisscross)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Examples](#examples)
  - [Usage](#usage)
    - [Commands](#commands)
    - [Process](#process)
      - [Example](#example)
      - [Options](#options)
    - [Combine](#combine)
      - [Example](#example-1)
      - [Options](#options-1)
    - [File Inclusion](#file-inclusion)
    - [Key-Value Pairs](#key-value-pairs)
  - [Roadmap](#roadmap)
  - [Built With](#built-with)
  - [Acknowledgments](#acknowledgments)
    - [Other related projects](#other-related-projects)
</details>

## Getting Started

### Prerequisites

- [Python 3](https://www.python.org/)
- (optional) [pandoc](https://github.com/jgm/pandoc), or [rmarkdown](https://github.com/rstudio/rmarkdown) are required to convert files from one format to another, crisscross requires either
- (optional) [LaTeX](https://www.latex-project.org/) is required for PDF generation

### Installation

```
pip3 install crisscross
```

## Examples

Here are some sample use cases of CrissCross, ordered by increasing complexity. 

- [English and Spanish](https://github.com/pnlng/crisscross/tree/master/examples/lang): Generate PDFs of the same file with keywords in different languages. 
- [PhD Applications](https://github.com/pnlng/crisscross/tree/master/examples/app): Generate personal statements customized for different schools. 
- [Weekly Quiz](https://github.com/pnlng/crisscross/tree/master/examples/quiz): Generate quizzes and their solutions for 2 different sections using the same template. 
  - The examples uses `crisscross combine` to take the "Cartesian product" of different sets of YAML metadata files, and `crisscross process` to generate PDF files from them. 

Here's a sneak peek of the [PhD applications](https://github.com/pnlng/crisscross/tree/master/examples/app) example. CrissCross allows you to go from a template that looks like this:

```markdown
!INCLUDE asis "examples/app/template.md"
```

To PDFs like these:

Michigan            |  UChicago
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/pnlng/crisscross/master/screenshots/michigan.png)  |  ![](https://raw.githubusercontent.com/pnlng/crisscross/master/screenshots/uchicago.png)


## Usage

### Commands

There are two commands, `process` and `combine`.

### Process

`process` is the command that processes the template files. 

#### Example

Convert `TEMPLATE.md` into PDF, using key-value pairs specified in `VARS.yaml`:

```shell
crisscross process TEMPLATE.md -y VARS.yaml -o OUTDIR/TEMPLATE.pdf
```
#### Options

```
!INCLUDE asis "help/process.md"
```

### Combine

`combine` is a helper command takes the "Cartesian product" of lists of files. 

#### Example

```shell
crisscross combine a1,a2 b1,b2 -o out/
```

would generate under `out/`

```
out/
  a1_b1
  a1_b2
  a2_b1
  a2_b2
```

where `a1_b1` is a concatenation of `a1` and `b1`, `a1_b2` a concatenation of `a1` and `b2`, and so on. 

See the [quiz](https://github.com/pnlng/crisscross/tree/master/examples/quiz) example for a real-world use case of `combine.`

#### Options

```shell
!INCLUDE asis "help/combine.md"
```

### File Inclusion

Two inclusion tags are supported:

- `!INCLUDE "foo.md"`, in the style of [Markdown Preprocessor](https://github.com/jreese/markdown-pp#includes), and
- `@import "foo.md"`, in the style of [Markdown Preview Enhanced](https://shd101wyy.github.io/markdown-preview-enhanced/#/file-imports)
  - However, unlike MPE, CrissCross does not support `<!-- @import "foo.md" -->`. 

Adding `asis` after the inclusion tag will tell CrissCross to include the file as is, and not to further process it: `!INCLUDE asis "foo.md"`

### Key-Value Pairs

Key-value pairs tell CrissCross how to replace placeholder expressions. They can be either placed in YAML files:

```yaml
!INCLUDE asis "examples/lang/custom/en.yaml"
```

Alternatively, they could be supply using the `-V` option:

```
crisscross process -V key1:value1 -V key2:value2 TEMPLATE -o OUTFILE
```

## Roadmap

- [ ] Add the option to render inline placeholders as is
- [ ] Add the option to use different patterns for placeholder expressions
- [ ] Add logic support

## Built With

This project uses the following open source libraries.

- [pallets/click](https://github.com/pallets/click): Python composable command line interface toolkit
- [hackebrot/poyo](https://github.com/hackebrot/poyo): A lightweight YAML Parser for Python
- [noahmorrison/chevron](https://github.com/noahmorrison/chevron): A Python implementation of mustache

## Acknowledgments

This project is heavily inspired by:

- [alpianon/include-pandoc](https://github.com/alpianon/include-pandoc): A wrapper for pandoc to pre-process includes
- [michaelstepner/pandoc-mustache](https://github.com/michaelstepner/pandoc-mustache): Pandoc filter for variable substitution using Mustache syntax
  
### Other related projects

- [jreese/markdown-pp](https://github.com/jreese/markdown-pp): Preprocessor for Markdown files to generate a table of contents and other documentation needs
- [DCsunset/pandoc-include](https://github.com/DCsunset/pandoc-include): Pandoc filter to allow file includes
- [owickstrom/pandoc-include-code](https://github.com/owickstrom/pandoc-include-code): A Pandoc filter for including code from source files
- [MrToph/pandoc-code-file-filter](https://github.com/MrToph/pandoc-code-file-filter): A filter for pandoc to include sections of code from a file
