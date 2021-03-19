import argparse
from datetime import datetime
import subprocess
import shutil
import zipfile

from config import *
from util.latex import make_quiz_id, make_args, latex_main
from util import ui

parser = argparse.ArgumentParser(description="Generates PDFs.")
parser.add_argument("num", type=int,
                    help="Number of unique PDFs to generate.")
parser.add_argument("--random", dest="random", action="store_true")
parser.add_argument("--soln", dest="is_soln", action="store_true")
parser.add_argument("--zip", dest="use_zip", action="store_true")
parser.add_argument("--force", "-f", dest="force", action="store_true")

def get_quiz_numbers(args):
  if args.num > TOTAL_NUM_QUIZZES:
    print("Error: number of quizzes specified exceeds {}".format(TOTAL_NUM_QUIZZES))
    print("This is specified in scripts/config.py and unique_rules.csv.")
    return []
  if args.random:
    print("Generating quizzes in random order. Uses random seed in config.py.")
    quiz_numbers = np.random.choice(np.arange(TOTAL_NUM_QUIZZES),
                      size=args.num, replace=False).tolist()
  else:
    quiz_numbers = np.arange(args.num).tolist()
  return quiz_numbers

def make_pdfs(quiz_numbers, is_soln, use_zip, force):
  prepare_output_directories(is_soln, use_zip)

  for quiz_number in quiz_numbers:
    quiz_id = make_quiz_id(quiz_number)
    print(">>>", quiz_id)
    pdf_dst = make_pdf(quiz_id, is_soln, force)
    if len(pdf_dst) == 0: # compilation had error
      print("Terminating.")
      break

    if use_zip:
      make_zip(quiz_id, pdf_dst, force)
  cleanup_output_directories()

def copy_unique_rules():
  unique_rules_src = QUIZ_RULE_PERMUTATIONS_CSV
  unique_rules_dst = "{}.{}.csv".format(
      QUIZ_RULE_PERMUTATIONS_CSV.split('.csv')[0],
      datetime.now().strftime("%Y%m%d%H%M"))

#####################################
def prepare_output_directories(is_soln, use_zip):
  pdf_dir = "pdfs" if not is_soln else "pdfs_soln"
  output_dirs = ["tex", "tex_aux", pdf_dir]
  if use_zip: output_dirs.append("zips")

  for output_dir in output_dirs:
    # make output directories if they don't exist
    Path(os.path.join(OUT_DIR, output_dir)).mkdir(
          parents=True, exist_ok=True)

def cleanup_output_directories():
  """Delete the tex_aux folder which is just pdflatex scratch space."""
  tex_aux_dir = os.path.join(OUT_DIR, "tex_aux")
  if os.path.exists(tex_aux_dir):
    shutil.rmtree(tex_aux_dir)


def make_pdf(quiz_id, is_soln, force):
  latex_main(make_args(quiz_id, is_soln=is_soln, is_template=False))

  pdf_fname, outstr = call_pdflatex(quiz_id, is_soln)
  if pdf_fname is None:
    print("\tpdflatex: Error for {}".format(quiz_id))
    print(outstr)
    return ""

  pdf_src = os.path.join(OUT_DIR, "tex_aux", pdf_fname)
  is_soln_str = "_soln" if is_soln else ""
  pdf_dst = os.path.join(OUT_DIR, "pdfs{}".format(is_soln_str),
                          pdf_fname)

  if not os.path.exists(pdf_src):
    print("Error: PDF not found: {}".format(pdf_fname))
    return ""
  if not os.path.exists(pdf_dst) or can_overwrite(pdf_fname, force):
    print("\tWrote PDF to {}".format(pdf_dst))
    shutil.copyfile(pdf_src, pdf_dst)
  else:
    print("\tDidn't write PDF.")
  return pdf_dst

def can_overwrite(fname, force):
  return force or  \
      ui.get_yes_or_no("\tWarning: Overwrite existing file {}?".format(
            fname), default='y')

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

def make_zip(quiz_id, pdf_dst, force):
  """
  Assume a PDF exists. Then makes a student-facing LaTeX template
  and creates a zip of .tex + .pdf files.
  """
  zip_dir = os.path.join(OUT_DIR, "zips")
  zip_name = "{}.zip".format(quiz_id)
  zip_dst = os.path.join(zip_dir, zip_name)
  if os.path.exists(zip_dst) and can_overwrite(zip_name, force):
    # remove existing zip file
    os.remove(zip_dst)
  Path(zip_dir).mkdir(parents=True, exist_ok=True)

  tex_src = latex_main(make_args(quiz_id, is_template=True))
  zf = zipfile.ZipFile(zip_dst, mode='w', compression=zipfile.ZIP_DEFLATED)
  try:
    zf.write(tex_src, "{}.tex".format(EXAM_NAME))
    zf.write(pdf_dst, "{}.pdf".format(EXAM_NAME))
  finally:
    zf.close()

  print("\tWrote zip to {}".format(zip_dst))

def main():
  args = parser.parse_args()
  quiz_numbers = get_quiz_numbers(args)
  if len(quiz_numbers) == 0:
    print("No quizzes generated.")
    return

  make_pdfs(quiz_numbers, args.is_soln, args.use_zip, args.force)
  if not args.is_soln:
    copy_unique_rules()

#####################################
if __name__ == "__main__":
  main()
