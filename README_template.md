# CrissCross

CrissCross is a Markdown-centric templating engine. 

Some of its features: 

- Replace Mustache-style placeholders `{{var}}`
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
    - [Basic Usage](#basic-usage)
    - [Commands](#commands)
    - [Process](#process)
    - [Combine](#combine)
</details>

## Getting Started

### Prerequisites

![](https://img.shields.io/pypi/pyversions/crisscross)

Crisscross requires Python 3.

To convert files from one format to another, crisscross requires either [pandoc](https://github.com/jgm/pandoc), or [rmarkdown](https://github.com/rstudio/rmarkdown).


### Installation

```
pip3 install crisscross
```

## Examples

Here are some sample use cases of CrissCross, ordered by increasing complexity. 

- [Recursive Inclusion](examples/lang): Generate PDFs of the same file with keywords in different languages. 
- [Graduate School Application](examples/app): Generate personal statements customized for different schools. 
- [Quiz](examples/quiz): Generate quizzes and their solutions for 2 different sections using the same template. 
  - The examples uses `crisscross combine` to take the "Cartesian product" of different sets of YAML metadata files, and `crisscross process` to generate PDF files from them. 

## Usage

### Basic Usage

Convert `TEMPLATE.md` into PDF, using key-value pairs specified in `VARS.yaml`:

```shell
crisscross process TEMPLATE.md -y VARS.yaml -o OUTDIR/TEMPLATE.pdf
```

### Commands

There are two commands, `process` and `combine`.

### Process

`process` is the command that processes the template files. 

```
!INCLUDE asis "help/process.md"
```

### Combine

`combine` is a helper command takes the "Cartesian product" of lists of files. 

```shell
!INCLUDE asis "help/combine.md"
```

