# LaTeX `src` folder
Two main files:
* `quiz02.tex`
* `quiz02_soln.tex` which makes some very small changes to `quiz02.tex`

Important files

For each problem (e.g., `bernoulli`)
* `bernoulli_defs.tex`: variable definitions
* `bernoulli_prob.tex`: problem statements that use the variables defined in `bernoulli_defs.tex`. These problem statements also specify the amount of whitespace, solution snippet files, etc. for each part of each problem.
* `bernoulli_soln_*.tex` solution snippet files.

Custom LaTeX commands:
* `quizblank_helper.tex`: LaTeX custom commands defined for blank problem statement PDFs. Called in `*_probs.tex` files.
* `quizsoln_helper.tex`: LaTeX custom commands based on those in `quizblank_helper.tex` which ignore whitespace and instead substitute in solution snippet files (see `scripts/util/latex.py` for implementation)

Template files:
* Student LaTeX template files are just one giant file with all of the raw LaTeX code for each student.
* To allow students to just edit one single file, the current Python script (`script/util/latex.py`) parses the custom LaTeX files and substitutes in the necessary LaTeX so that students know what to edit.
* Note: We should change this so it's more general. Alternatively we should create a Python-free `quiztemplate_helper.tex` file that's editable by instructors that is separately parsed by Python.

# Run everything
```
python3 scripts/generate_permutations.py

./scripts/generate_pdfs.sh # calls generates_latex.py and pdflatex

./scripts/make_students.sh # makes all student zip files
```

# Setting permutable values in `src/variables.csv`

Variables can either be selected from a list of values or functions of other variables. 
* **Independent parameters**: Specify possible values
* **Dependent parameters**: Write as a function of other existing variables.

Variables vary as follows:
* By default, `itertools.product` will read in the variables in row-order and vary according to that order. In other words, the first variable listed in a question will be varied the least, and the last variable will be varied the most.
* To adjust this order, set column 3 (VARIABILITY). Larger number means varied more.
* A variability of 0 means that the variable will not be included in the variation. Note that functions of variables are not included by default.
* **Lock-step parameters**: Variables can also vary **in lock step** with other variables by setting column 4 (VARSYNC). For example, if TOTROOMTIME has VARSYNC=ROOMTWO, then ROOMTWO will vary, and then the i-th value of ROOMTWO will always correspond to the i-th value of TOTROOMTIME. Note the VARIABILITY for TOTROOMTIME should be set to 0. You may choose to specify parameters as lock-step parameters if you want to reduce the number of exam permutations but you still want unique numbers.

Columns:
* `VARNAME`: Variable name. Leave blank if this row does not define any new variables, i.e., is just used for a constraint.
* `PROBLEM`: Problem name.
* `VARIABILITY`: If this row creates an independent parameter, you can specify what order this variable should be varied in with respect to `itertools.product` (see above).
* `VARSYNC`: Sometimes you may not want independent parameters to be varied with respect to `itertools.product` -- instead, you might want them to move in lock-step with other independent parameters. This independent parameter will move in lock-step with the variable specified in this column, if it exists (otherwise it will be incorporated as part of `itertools.product`.
* `SOLN`: `1` if part of the compiled solution PDF; `0` if part of the compiled problem statement PDF.
* `FUNCTION`: If a dependent parameter, contains the Python function by which to generate this value. If a constraint, contains the Python boolean expression that must evaluate to True.
* Beyond `FUNCTION`: Any values associated with this independent parameter.

Function writing:
* Should be written with Python syntax. Any functions called by external Python libraries must be specified in `scripts/config.py`'s `FUNC_MAP`.
* The functions written in the `FUNCTION` column will be evaluated using the `cexprtk` package, which requires any non-native Python functions to be specifeid using a function map like `FUNC_MAP`.

# Student submission lookup
* There should be some sort of Student to Student ID file somewhere in this directory (we can make a bogus one).
* `scripts/make_lookup.py` creates the lookup, which is randomized but repeatable (i.e., seeded).

# Install Requirements
Install requirements for python libraries:
`pip install -r requirements.txt`.  
