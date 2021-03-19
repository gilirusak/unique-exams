"""
Description: generates latex for unique quizzes
Author: Gili Rusak and Lisa Yan
Jan 13, 2021
"""
import argparse

from config import *
from util.latex_helper import read_template

def make_quiz_id(quiz_number):
  return str(quiz_number).zfill(4)

def get_template(args):
  if args.is_soln:
    return EXAM_SOLN_TEMPLATE
  return EXAM_TEMPLATE

def load_permutations_file():
  # get unique numbers for student number quiz_number
  with open(QUIZ_RULE_PERMUTATIONS_CSV, 'r', encoding="utf8") as f:
    rules_array = np.genfromtxt(['\t'.join(tup) \
                      for tup in csv.reader(f, delimiter=',', quotechar='"')],
                             delimiter='\t',
                             dtype=str)

  # return header and student rows
  return rules_array[0,:], rules_array[1:]

def prepare_headers(args):
  headers, _ = load_permutations_file()
  if not args.is_template:
    # we are reading in the *_defs.tex files, so our magic_template
    # should replace the constants in *_defs.tex files
    headers = ["{}_VALUE".format(header) for header in headers]
  else:
    # we will not read in any *_defs.tex files,
    # so we will directly replace the constant to be the variable name.
    # LaTeX prepends a forward slash (\) to all variable names.
    headers = ["\\{}".format(header) for header in headers]

  return headers

def prepare_exam_path(quiz_id, args):
  exam_dir = TEX_PATH_DIR

  if args.is_template:
    exam_dir += "_template"
    exam_name = "{}_template_{}".format(EXAM_NAME, quiz_id)
  else:
    if args.is_soln:
      exam_dir += "_soln"
    exam_name = "{}_{}".format(EXAM_NAME, quiz_id)
    if args.is_soln:
      exam_name += "_soln"

  Path(exam_dir).mkdir(parents=True, exist_ok=True)

  exam_path = os.path.join(exam_dir, "{}.tex".format(exam_name))
  return exam_path

def get_quiz_rule(quiz_number):
  # safety checks
  assert(quiz_number >= 0 and quiz_number < TOTAL_NUM_QUIZZES)

  # row 1 is default quiz with index 0
  _, rules_array = load_permutations_file()

  unique_rule = rules_array[quiz_number]
  return unique_rule

def get_examid_key(args):
  if args.is_template:
    return "\\EXAMID"
  else:
    return "EXAMID_VALUE"

############################# main ############################################

def make_args(quiz_number=None, is_soln=False, is_template=False):
  """
  Handles both calls from command-line and another python file.
  """
  parser = argparse.ArgumentParser(description="Generates LaTeX documents.")
  parser.add_argument("quiz_number", type=int,
                      help="Quiz number to generate")
  parser.add_argument("--soln", dest="is_soln", action="store_true",
                      help="Flag for creating solution document")
  parser.add_argument("--template", dest="is_template", action="store_true",
                        help="Flag for creating template document")

  args_list = []
  if quiz_number is not None:
    args_list.append(str(quiz_number))
  if is_soln:
    args_list.append("--soln")
  if is_template:
    args_list.append("--template")
  return parser.parse_args(args_list)

def latex_main(args):
  quiz_number = args.quiz_number          # get exam number
  quiz_id = make_quiz_id(quiz_number)

  headers = prepare_headers(args)

  unique_rule = get_quiz_rule(quiz_number)
  assert(len(unique_rule) == len(headers))

  # read tex template
  template = read_template(get_template(args), TEMPLATE_PATH_DIR, args)

  magic_template = template
  # find and replace each value of header
  for i, INPUT_KEY in enumerate(headers):
    magic_str = unique_rule[i]
    if args.is_template:
      # could have multiple occurrences, since we are not using def
      # first remove any empty arg calls
      magic_template = magic_template.replace(INPUT_KEY + "{}", INPUT_KEY)
      magic_template = magic_template.replace(INPUT_KEY, str(magic_str))
    else:
      # each variable should only be defined once. If there's
      # multiple definitions, everything collapses.
      assert(template.count("{" + INPUT_KEY) <= 1) # in case substrings
      magic_template = magic_template.replace(INPUT_KEY, str(magic_str), 1)

  # if there is an EXAMID field, fill it in
  magic_template = magic_template.replace(get_examid_key(args), quiz_id, 1)

  # write new tex file
  exam_path = prepare_exam_path(quiz_id, args)
  with open(exam_path, 'w') as writer:
    writer.write(magic_template)
    print("\tWrote LaTeX template to", writer.name)
  return exam_path
