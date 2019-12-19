CC = crisscross
CCP = $(CC) process
CCPPLAIN = $(CCP) --no-yaml --no-render
EXDIR = examples
APPDIR = $(EXDIR)/app
QUIZDIR = $(EXDIR)/quiz
LANGDIR = $(EXDIR)/lang
README = README.md
READMETEMP = README_template.md

exdoc:
	cd $(APPDIR) && \
	$(CCPPLAIN) $(READMETEMP) -o $(README)
	cd $(LANGDIR) && \
	$(CCPPLAIN) $(READMETEMP) -o $(README)
	cd $(QUIZDIR) && \
	$(CCPPLAIN) $(READMETEMP) -o $(README)

app:
	cd $(APPDIR) && \
	$(CCP) header.md template.md

lang:
	cd $(LANGDIR) && \
	$(CCP) a.md -o out/{{id}}.pdf

quiz:
	cd $(QUIZDIR) && \
	$(CC) combine yaml/101.yaml,yaml/102.yaml yaml/orig.yaml,yaml/soln.yaml -o yaml_combined/ && \
	$(CCP) -V number:1 -V date:'Jan 1 2001' -y 'yaml_combined/*.yaml' template.md -o quizzes/quiz{{number}}_{{id}}.pdf -r rmarkdown

maindoc:
	$(CC) process -h > help/process.md
	$(CC) combine -h > help/combine.md
	$(CCPPLAIN) $(READMETEMP) -o $(README)

docs: exdoc maindoc

all: app quiz lang docs

pypi:
	rm -rf dist
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*