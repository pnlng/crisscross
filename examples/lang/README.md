# Example: Recursive Inclusion

This simple example demonstrates CrissCross's ability to recursively include files. 

I want to create a PDF in both English and Spanish, and my template files contains "recursive" inclusion statements. 

## Templates

The top level file is `a.md`:

```markdown
{{level}} A

!INCLUDE "b.md"

{{level}} A
```

It references `b.md`:

```markdown
{{level}} B

!INCLUDE "custom/final_{{id}}.md"

{{level}} B
```

And `b.md` in turn references `custom/final_compiled.md`. The reference will be dynamically resolved. `compiled` will by default take the value of the current YAML file. 

For example, for the YAML file `en.yaml`, our `compiled` will be replaced by `en`. So we'll be including `final_en.md`:

```markdown
This is the final level.

Yay!
```

## Variables in YAML

I have two YAML files under `custom/`.

```
custom/
    en.yaml
    es.yaml
```

Each contains a set of variables to replace the placeholder expressions `` and `` in my template files. 

```
lang: English
level: Level
```
## Conversion

I run the following command. 

```shell
crisscross process a.md -o out/compiled.pdf
```

By default, CrissCross takes all YAML files placed under `custom/`. The command specifies that the generated files should be placed under `out/`. ``compiled`` is a placeholder expression whose default value is the name of the YAML file used. So for the English files, it will be replace by ``en``.

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
Level A

Level B

This is the final level.

Yay!

Level B

Level A
```

We've made use of some of the options of the `process` command in this example. For other uses, please see the [main documentation](../../) for more details.
