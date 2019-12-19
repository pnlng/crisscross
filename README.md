# CrissCross

CrissCross is a Markdown-centric templating engine. 

Some of its features: 

- Replace Mustache-style placeholders ``
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
Usage: crisscross process [OPTIONS] TEMPLATES...

  Preprocess text files, and render with pandoc or rmarkdown.

Options:
  -y, --yaml PATH                 The YAML file(s) to be used. If wildcard
                                  characters are used, then the whole argument
                                  must be quoted, e.g., -y '*.yaml'.
                                  (Default: custom/*.yaml)
  --no-yaml                       Use no YAML files. In this case, key-value
                                  pairs must be supplied with -k --key-value.
                                  (Default: disabled)
  -o, --out PATH                  Schema for the path to an output file.
                                  Variables are accepted. 
                                  (Default:
                                  docs/{{id}}.pdf)
  --open-ren / --no-open-ren      Whether to open the rendered files
                                  automatically. 
                                  (Default: enabled)
  --open-text / -no-open-text     Whether to open the generated text files
                                  automatically. 
                                  (Default: disabled)
  -a, --args TEXT                 A string of arguments to be passed on to
                                  pandoc. Passing arguments to rmarkdown not
                                  supported. If there are spaces, the string
                                  should be quoted.
  -r, --render [pandoc|rmarkdown]
                                  Render using vanilla pandoc or rmarkdown, or
                                  do not render at all. 
                                  (Default: pandoc)
  --no-render                     Do not render the files with pandoc or
                                  rmarkdown. Only do variable substitution or
                                  file inclusion. 
                                  (Default: disabled)
  --include-tag [include|import]  Syntax for file inclusion. Either !INCLUDE
                                  "filename" or @import "filename". 
                                  (Default:
                                  include)
  -V, --variable TEXT             A key-value pair separated by ":". No spaces
                                  allowed. Can be used in conjunction with or
                                  in place of YAML files.
  -f, --force                     Suppress warnings. 
                                  (Default: disabled)
  -q, --quiet / -v, --verbose     Suppress messages. 
                                  (Default: disabled)
  -h, --help                      Show this message and exit.
```

### Combine

`combine` is a helper command takes the "Cartesian product" of lists of files. 

```shell
Usage: crisscross combine [OPTIONS] [FILES]...

  Generate the 'Cartesian product' of multiple files.

Options:
  -o, --out DIRECTORY          Output directory.
  -s, --separator TEXT         Character used to join the names of input
                               files.
  -q, --quiet / -v, --verbose  Suppress messages. 
                               (Default: disabled)
  -h, --help                   Show this message and exit.
```
