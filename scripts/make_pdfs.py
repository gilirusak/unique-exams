import argparse
import subprocess
from datetime import datetime
import shutil

from config import *
from util.generate_latex import make_quiz_id, make_args, latex_main

parser = argparse.ArgumentParser(description="Generates PDFs.")
parser.add_argument("num", type=int,
                    help="Number of unique PDFs to generate.")
parser.add_argument("--random", dest="random", action="store_true")
parser.add_argument("--soln", dest="is_soln", action="store_true")

def get_quiz_numbers(args):
  if args.num > TOTAL_NUM_QUIZZES:
    print("Error: number of quizzes specified exceeds {}".format(TOTAL_NUM_QUIZZES))
    print("This is specified in scripts/config.py and unique_rules.csv.")
    return []
  if args.random:
    quiz_numbers = np.random.choice(np.arange(TOTAL_NUM_QUIZZES),
                      size=args.num, replace=False).tolist()
  else:
    quiz_numbers = np.arange(args.num).tolist()
  return quiz_numbers

def make_pdfs(quiz_numbers, is_soln=False):
  if len(quiz_numbers):
    prepare_output_directories(is_soln)

  for quiz_number in quiz_numbers:
    quiz_id = make_quiz_id(quiz_number)
    print(">>>", quiz_id)
    success = make_pdf(quiz_id, is_soln)
    if not success:
      print("Terminating.")
      break

def copy_unique_rules():
  unique_rules_src = "unique_rules.csv"
  unique_rules_dst = "unique_rules.{}.csv".format(
      datetime.now().strftime("%Y%m%d%H%M"))

#####################################33
def prepare_output_directories(is_soln):
  pdf_dir = "pdfs"
  if is_soln: pdf_dir += "_soln"
  for output_dir in ["tex", "tex_aux", pdf_dir]:
    # make output directories if they don't exist
    Path(os.path.join(OUT_DIR, output_dir)).mkdir(
          parents=True, exist_ok=True)

def make_pdf(quiz_id, is_soln):
  latex_main(make_args(quiz_id, is_soln=is_soln, is_template=False))

  pdf_fname, outstr = call_pdflatex(quiz_id, is_soln)
  if pdf_fname is None:
    print("\tpdflatex: Error for {}".format(quiz_id))
    print(outstr)
    return False

  pdf_src = os.path.join(OUT_DIR, "tex_aux", pdf_fname)
  is_soln_str = "_soln" if is_soln else ""
  pdf_dst = os.path.join(OUT_DIR, "pdfs{}".format(is_soln_str),
                          pdf_fname)

  if os.path.exists(pdf_src):
    if os.path.exists(pdf_dst):
      print("\tWarning: Overwriting previous PDF for {}".format(
            pdf_fname))
    print("\tWrote PDF to {}".format(pdf_dst))
    shutil.copyfile(pdf_src, pdf_dst)
    return True
  else:
    print("Error: PDF not found: {}".format(pdf_fname))
    return False

def call_pdflatex(quiz_id, is_soln):
  temp_dir = os.path.join(OUT_DIR, "tex_aux")
  is_soln_str = "_soln" if is_soln else ""
  exam_name = "{}_{}{}".format(EXAM_NAME, quiz_id, is_soln_str)

  tex_src = os.path.join(OUT_DIR, "tex{}".format(is_soln_str),
                         "{}.tex".format(exam_name))

  cmd = [
      "pdflatex",
      "-halt-on-error",                 # quits if error
      "-interaction=nonstopmode",       # quits when file not found
      "-output-directory={}".format(temp_dir),
      "-shell-escape", tex_src
      ]
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
  output, error = process.communicate()
  cmd_repeat = "\nTo rerun on command-line:\n{}".format(' '.join(cmd))
  outstr = output.decode() + cmd_repeat
  if error is not None or "Fatal error occurred" in outstr:
    return None, outstr
  return "{}.pdf".format(exam_name), outstr

def main(is_soln=False):
  args = parser.parse_args()
  if is_soln:           # called from make_solutions.py, so explicit set
    args.is_soln = True

  quiz_numbers = get_quiz_numbers(args)
  make_pdfs(quiz_numbers, args.is_soln)
  if not args.is_soln:
    copy_unique_rules()

#####################################33
if __name__ == "__main__":
  main(is_soln=False)
