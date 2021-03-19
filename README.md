# Installation: Requirements
* `pdflatex`
* `python3`
* Install requirements for python libraries: `pip install -r requirements.txt` which installs `numpy`, `scipy`, and `asteval`. The last of these is the Python expression interpreter we use for reading and generating dependent parameters (more [here](http://newville.github.io/asteval/)).

# Overview: Generating exams
1. `python3 scripts/make_permutations.py` generates the permutations CSV, `unique_rules.csv`.
1. `python3 scripts/make_pdfs.py 1` to make a single test item. To make ten in sequential order, `python3 scripts/make_pdfs.py 10`.
    * You can add `-f`or `--force` to force overwrite of existing PDFs/zip files.
    * You can add `--zip` to make zip folders that contain both the exam PDF and a student-facing exam template in LaTeX.
    * To make a random set, add `--random`. This may be useful if you want to check a random set of exams for correctness. Note the random seed is in `scripts/config.py` so that you can reliably check the same set of 5 exams across edits.
1. `python3 scripts/make_pdfs.py N --soln` to make all solution files (`N` is the number of exams). 
1. `python3 scripts/make_lookup.py` randomly assigns students to quiz IDs and stores the lookup in `student_lookup.csv`.

Input files/directories:
* `variables.csv` contains the parameter definitions for both independent parameters (the set of possible values) and dependent parameters (the function to generate the values).
* `src` is the LaTeX source file folder for your exam.
* `roster.csv` contains the list of students to assign to exams.
* `scripts/config.py` defines filenames, max number of quizzes, problem names, etc.

Output files/directories:
* `unique_rules.csv` contains all permutations to generate exams.
* `output/pdfs` contains blank exam PDFs by ID.
* `output/tex` contains tex to generate exam PDFs.
* `output/tex_template` contains LaTeX templates to distribute to students (`--zip` flag)
* `output/zips` contains zips of exam PDFs + student LaTeX templates (`--zip` flag)
* `student_lookup.csv` contains student to pseudorandom Quiz ID, as well as associated permutation row for easy grading.

# 1. Edit the LaTeX source in `src`
Two main files:
* `src/quiz.tex`, which compiles to the exam PDF
* `src/quiz_soln.tex` which compiles to the exam solution PDF
* **Note**: The `quiz.pdf` or `quiz_soln.pdf` in this folder are *not* unique exams and are included for convenience. You can directly compile the above two files into this directory to iterate on the exam content before you run the above Python scripts to generate the unique batch of exams.

For each problem (e.g., `binomial`)
* `src/problems/binomial_defs.tex`: variable definitions that connect those written in `variables.csv` to those written in the LaTeX templates.
* `src/problems/binomial_prob.tex`: problem statements that use the variables defined in `binomial_defs.tex`. These problem statements also specify the amount of whitespace, solution snippet files, etc. for each part of each problem.
* `src/problems/binomial_soln.tex` solution snippet file.

Custom LaTeX commands:
* `src/quizblank_helper.tex`: LaTeX custom commands defined for blank problem statement PDFs. Called in `*_probs.tex` files.
* `src/quizsoln_helper.tex`: LaTeX custom commands based on those in `quizblank_helper.tex` which ignore whitespace and instead substitute in solution snippet files (see `scripts/util/latex.py` for implementation)

Template files:
* Student LaTeX template files are just one giant file with all of the raw LaTeX code for each student.
* To allow students to just edit one single file, the current Python script (`script/util/latex.py`) parses the custom LaTeX files and substitutes in the necessary LaTeX so that students know what to edit.

# 2. Set parameter values in `src/variables.csv`

Variables can either be selected from a list of values or functions of other variables.
* **Independent parameter**: Specify possible preset values.
* **Dependent parameter**: Write as a function of other existing variables.
* **Conditional parameter**: Assert that the parameter combinations make sense in the context of the problem, i.e., a constraint
* **Solution parameter**: Computed as needed for the solution key.
* By default, `scripts/make_permutations.py` will read in the variables in row-order and vary according to that order. In other words, the first variable listed in a question will be varied the least, and the last variable will be varied the most.
* **Lock-step parameters**: Variables can also vary **in lock-step** with other variables by setting the VARSYNC column. For example, if NB
 has NA in the VARSYNC column, then NA will vary as an independent parameter, and then the i-th value of NB will always correspond to the i-th value of NA. You may choose to specify parameters as lock-step parameters if you want to reduce the number of exam permutations but you still want unique numbers.

`variables.csv` columns:
* `VARNAME`: Variable name. Leave blank if this row does not define any new variables, i.e., is just used for a constraint (i.e., conditional parameter).
* `PROBLEM`: Problem name. This must correspond to a valid string in the `PROBLEMS` variable of `scripts/config.py`.
* `VARSYNC`: Sometimes you may not want independent parameters to be varied with respect to `itertools.product` -- instead, you might want them to move in lock-step with other independent parameters. This independent parameter will move in lock-step with the variable specified in this column, if it exists (otherwise it will be incorporated as part of `itertools.product`.
* `SOLN`: `1` if part of the compiled solution PDF; `0` if part of the compiled problem statement PDF.
* `FUNCTION`: If a dependent parameter, contains the Python function by which to generate this value. If a constraint, contains the Python boolean expression that must evaluate to True.
* Beyond `FUNCTION`: Any values associated with this independent parameter.

Function writing:
* Should be written with Python syntax. 
* To specify custom functions, define them in `helper_function.py`. For example, `mystery` is defined in `helper_functions.py` and then loaded into the `FUNC_MAP` dictionary, which is then loaded into the asteval interpreter.

# 3. Generate a student exam lookup
* The `roster.csv` contains a dummy roster that contains the columns titled Name, ID, and Email.
* The generated `student_lookup.csv` contains a pseudorandom assignment of students to Quiz ID numbers:
  * A random seed in `scripts/config.py` allows you that you can reliably update and edit your LaTeX source or parameter values and regenerate exams/regenerate this lookup table.
  * You need to have had run `scripts/make_pemrutations.py` first which will create the unique parameter tuples in `unique_rules.csv`.
  * The resulting table includes a lookup of all intermediate parameter values that you can use while grading.

# Credit
This tool was released as part of the following publication. If you clone or edit this tool, we ask that you please cite the following:

Gili Rusak and Lisa Yan. 2021. "Unique Exams: Designing Assessments for Integrity and Fairness." In Proceedings of the 52nd ACM Technical Symposium on Computer Science Education (SIGCSE '21). Association for Computing Machinery, New York, NY, USA, 1170–1176. <a href="https://doi.org/10.1145/3408877.3432556" target="_blank">https://doi.org/10.1145/3408877.3432556</a>

Author contact: Lisa Yan (yanlisa@stanford.edu), Gili Rusak (gili@stanford.edu)


