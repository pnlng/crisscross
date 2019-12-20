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
  --open-text / --no-open-text    Whether to open the generated text files
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
