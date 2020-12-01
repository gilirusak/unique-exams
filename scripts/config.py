import os
from scipy import stats, special

# file constants
TOTAL_NUM_QUIZZES = 10
QUIZ_RULE_PERMUTATIONS_CSV = "unique_rules.csv"
EXAM_NAME = "quiz_test"
OUT_DIR = "output"

TEMPLATE_PATH_DIR = "src" # where EXAM_TEMPLATE and EXAM_SOLN_TEMPLATE are located
EXAM_TEMPLATE =  "quiz_example.tex"
EXAM_SOLN_TEMPLATE =  "quiz02_soln.tex"
TEX_PATH_DIR = os.path.join(OUT_DIR, "tex")
VARIABLES_FNAME = "variables_paper.csv"
UNIQUE_RULES_FNAME = "unique_rules.csv"

# should correspond to the order of the problems in your exam
PROBLEMS = ['problem1', 'problem2', 'problem3']

from scripts import helper_functions
# functions that you call in variables.csv. Must be associated
# with real python functions, otherwise you should define them.
# needed especially if you use any packages.
FUNC_MAP = {
      "poisson_pmf": stats.poisson.pmf,
      "binom_pmf": stats.binom.pmf,
      "norm_pdf": stats.norm.pdf,
      "binom": special.binom,
      "intcast": helper_functions.cast_int,
      "dummy": helper_functions.dummy,
      "phi": helper_functions.phi,
      "right_bitshift": helper_functions.right_bitshift,
      "pipe": helper_functions.pipe
    }

# write any additional helper functions here.
# in particular, if you just want to write your own helper function
# specific to a function, write it in scripts/helper_functions.py
# and map it in this QUESTION_MAP.
QUESTION_MAP = {
    # if I want the question named bernoulli to be generated
    # from the function bernoulli_rules
    # "bernoulli": helper_functions.bernoulli_rules
    }
