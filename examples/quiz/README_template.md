# Example: Weekly Quiz

This example is an advanced use case of CrissCross. 

Suppose I teach two sections of the same course, 101 and 102. Each week, I'll quiz my students on the math they've learned. Afterwards, I'll give them a copy of the solutions. The two sections will receive different versions of the quiz each week. 

Here are the results I want:

Section 101 Original            |  Section 102 Original
:-------------------------:|:-------------------------:
![](../../screenshots/quiz1_101.png)  |  ![](../../screenshots/quiz1_102.png)

Section 101 Solutions            |  Section 102 Solutions
:-------------------------:|:-------------------------:
![](../../screenshots/quiz1_101_soln.png)  |  ![](../../screenshots/quiz1_102_soln.png)

## The Problem

For each version, I'd like to write the questions and solutions in a single file. (The reasons are a) it'll easier for me to keep track of the questions when I write the solutions, and b) students will be able to contextualize the solutions when they receive my answer key.) I decide to use the LaTeX package [`comment`](https://www.ctan.org/pkg/comment) together with CrissCross to control whether the solutions will be shown in my PDF.  

Therefore, each week, I'll create 4 different PDFs, based on combinations of the following 2 variables. 

- Section: 101 or 102
- Solutions: Yes or No


## Combine YAML

First, I create 4 YAML files under `yaml/`.

```
yaml/
    101.yaml
    102.yaml
    orig.yaml
    soln.yaml
```

For example, `101.yaml` contains the configurations for one section. 

```YAML
!INCLUDE asis "yaml/101.yaml"
```

On the other hand, `orig.yaml` contains specifies that solutions should not be included. 

```YAML
!INCLUDE asis "yaml/orig.yaml"
```

What I need is the Cartesian product of the YAML files, i.e., 4 YAML files each of which contains one of `(101.yaml, 102.yaml)` and one of `(orig.yaml, soln.yaml)`. We could copy and paste, but I'll use the `combine` function of CrissCross. The following command generates the desired YAML files under `yaml_combined`.

```shell
crisscross combine yaml/101.yaml,yaml/102.yaml yaml/orig.yaml,yaml/soln.yaml -o yaml_combined/
```

Note that there are no spaces before or after the commas. 

Now I get the combined YAML files. 

```
yaml_combined/
    101_orig.yaml
    101_soln.yaml
    102_orig.yaml
    102_soln.yaml
```

And `101_orig.yaml`, say, would just be a concatenation of `101.yaml` and `orig.yaml`.

```
!INCLUDE asis "yaml_combined/101_orig.yaml"
```

## Create Template

`template.md` is the master template I'll be using throughout the semester. It makes reference to the week number and the section number of my quiz. 

```
!INCLUDE asis "template.md"
```

Quiz 1 for section 101 looks like this:

```
!INCLUDE asis "quiz1_base_101.md"
```


## Convert

We're finally ready to generate the quiz files. 

```
crisscross process -y yaml_combined/*.yaml -V number:1 -V date:'Jan 1, 2001' template.md -o quizzes/quiz{{number}}_{{id}}.pdf -r rmarkdown
```

Here's a breakdown of the command:

- `-y yaml_combined/*.yaml` specifies the sets of variables to use. 
- `-V number:1` gives CrissCross an additional temporary variable-key pair.         - Along with `-V date:'Jan 1, 2001'`, it will be combined with each set of variables specified in the YAML files. 
- `-o quizzess/quiz{{number}}_{{id}}.pdf` indicates the directory and filename of my output files. 
  - ``{{id}}`` is a placeholder expression whose default value is the name of the YAML file used, e.g., `101_orig`.
- `-r rmarkdown` tell CrissCross to render using rmarkdown, instead of vanilla pandoc. 
  - The reason why I'm using rmarkdown is that I'd like to keep the intermediary LaTeX files. I can do that through rmarkdown, by specifying `keep_tex: true` in the YAML metadata block. 

I now have everything under `quizzes/`.

```
quizzes/
    quiz1_101_orig.md
    quiz1_101_orig.pdf
    quiz1_101_orig.tex
    ...
    quiz1_102_soln.md
    quiz1_102_soln.pdf
    quiz1_102_soln.tex
```

The results:

Section 101 Original            |  Section 102 Original
:-------------------------:|:-------------------------:
![](../../screenshots/quiz1_101.png)  |  ![](../../screenshots/quiz1_102.png)

Section 101 Solutions            |  Section 102 Solutions
:-------------------------:|:-------------------------:
![](../../screenshots/quiz1_101_soln.png)  |  ![](../../screenshots/quiz1_102_soln.png)

Next week, I will only need to create `quiz2_base_101.md` and `quiz2_base_102.md`, and modify my command a little bit, by using `-V number:2 -V date:'Jan 8, 2001'`. 

Since I teach for many many weeks in a semester, all the hassle is worth it! Phew!