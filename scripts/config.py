import csv
from pathlib import Path
from util.header import *             # also sets seed
from helper_functions import FUNC_MAP # custom parameter functions

# filenames
TOTAL_NUM_QUIZZES = 360
QUIZ_RULE_PERMUTATIONS_CSV = "unique_rules.csv"
EXAM_NAME = "quiz"        # what the PDFs are called
OUT_DIR = "output"        # directory to store PDFs

TEMPLATE_PATH_DIR = "src" # EXAM_TEMPLATE and EXAM_SOLN_TEMPLATE locations
EXAM_TEMPLATE =  "quiz.tex"
EXAM_SOLN_TEMPLATE =  "quiz_soln.tex"
TEX_PATH_DIR = os.path.join(OUT_DIR, "tex")

PROBLEMS = ['binomial', 'jointpdf', 'code']  # the order of problems in exam
VARIABLES_FNAME = "variables.csv"
UNIQUE_RULES_FNAME = "unique_rules.csv"

ROSTER_FPATH = "roster.csv"
STUDENT_LOOKUP = "student_lookup.csv"
