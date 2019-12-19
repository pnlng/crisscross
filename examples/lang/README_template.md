
# Example: Recursive Inclusion

This simple example demonstrates CrissCross's ability to recursively include files. 

I want to create a PDF in both English and Spanish, and my template files contains "recursive" inclusion statements. 

## Templates

The top level file is `a.md`:

```markdown
!INCLUDE asis "a.md"
```

It references `b.md`:

```markdown
!INCLUDE asis "b.md"
```

And `b.md` in turn references `custom/final_{{id}}.md`. The reference will be dynamically resolved. `{{id}}` will by default take the value of the current YAML file. 

For example, for the YAML file `en.yaml`, our `{{id}}` will be replaced by `en`. So we'll be including `final_en.md`:

```markdown
!INCLUDE asis "custom/final_en.md"
```

## Variables in YAML

I have two YAML files under `custom/`.

```
custom/
    en.yaml
    es.yaml
```

Each contains a set of variables to replace the placeholder expressions `{{lang}}` and `{{level}}` in my template files. 

```
!INCLUDE asis "custom/en.yaml"
```
## Conversion

I run the following command. 

```shell
crisscross process a.md -o out/{{id}}.pdf
```

By default, CrissCross takes all YAML files placed under `custom/`. The command specifies that the generated files should be placed under `out/`. ``{{id}}`` is a placeholder expression whose default value is the name of the YAML file used. So for the English files, it will be replace by ``en``.

We now have all the desired files. 

```
out/
    en.md
    en.pdf
    es.md
    es.pdf
```

And `en.md` looks like this:

```
!INCLUDE asis "out/en.md"
```

We've made use of some of the options of the `process` command in this example. For other uses, please see the [main documentation](../../) for more details. 