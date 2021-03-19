"""
Author: Lisa Yan October 5, 2020

Like making templates for problem sets, 
parses a particular tex file and writes out all text
into a single, compilable LaTeX file.
"""

import os
import re
import shutil

def read_template(template_fpath, dirname, args):
  return ''.join(read_template_lines(template_fpath, dirname, args), )

def read_template_lines(template_fpath, dirname, args):
  template_lines = []
  with open(os.path.join(dirname, template_fpath), 'r', encoding="utf8") as f:
    for line in f.readlines():
      if is_input_line(line):
        # load content in from another tex file
        addtl_fname = get_input_fname(line)
        if not addtl_fname.endswith(".tex"):
          if addtl_fname.startswith("#"): # this is part of some argument function
            template_lines.append(line)
            continue
          addtl_fname = "{}.tex".format(addtl_fname)
        if is_def_file(addtl_fname):
          # file is *_defs.tex
          if args.is_template:
            # don't load for student template
            continue

          template_lines += process_def_file_lines(addtl_fname, dirname)
        elif is_handwritten_file(addtl_fname):
          # file is quizblank_*.tex
          if args.is_template:
            # don't load for student template
            continue
          template_lines += read_template_lines(addtl_fname, dirname, args)
        elif is_solnwritten_file(addtl_fname):
          template_lines += placeholder_soln_lines()
        else:
          # copy external file text directly into this template
          template_lines += read_template_lines(addtl_fname, dirname, args)
      elif is_answer_space(line):
        if args.is_template:
          # for student template, substitute for shaded block option
          template_lines += shaded_block(line, dirname, args)
        elif args.is_soln:
          template_lines += shaded_answer_block(line, dirname, args)
        else:
          template_lines += blank_answer_block(line, dirname, args)
      elif is_pagebreak(line):
        # only append pagebreak if blank PDF
        if not(args.is_template or args.is_soln):
          template_lines.append(line)

      else:
        template_lines.append(line)
  return template_lines

def strip_line(line):
  line = line.split('%')[0] # exclude comments
  return line.strip()

def is_input_line(line):
  return strip_line(line).startswith("\\input{")

def get_input_fname(line):
  return line.split("\\input{")[-1].split('}')[0]

def is_def_file(fpath):
  return fpath.strip(".tex").endswith("_defs")

def is_handwritten_file(fpath):
  return fpath.startswith("quizblank")

def is_solnwritten_file(fpath):
  return fpath.startswith("quizsoln")

def is_answer_space(line):
  return strip_line(line).startswith("\\answer")

def is_pagebreak(line):
  return strip_line(line).startswith("\\problempagebreak")

def process_def_file_lines(template_fpath, dirname):
  """
  For all newcommands in this file, replace the defined value with
  the argument name + _VALUE, without the leading forward slash.
  ex: \newcommand{\XUBOUND}{3} --> \newcommand{\XUBOUND}{XUBOUND_VALUE}
  """
  def_lines = ['\n']
  with open(os.path.join(dirname, template_fpath), 'r') as f:
    for line in f.readlines():
      regex = r"\{(.*?)\}"
      params = re.findall(regex, line)
      if len(params) == 2:
        argname, argval = params
        def_lines.append("\\newcommand{{{}}}{{{}}}\n".format(
                          argname, "{}_VALUE".format(argname.strip('\\'))))
      else:
        def_lines.append(line)

  def_lines += ['\n']
  return def_lines 

def shaded_block(line, dirname, args):
  # for student templates
  shaded_block_lines = [
    "    \\begin{shaded}\n",
    "\n"
    ]
  # the below puts in the answer block too
  shaded_block_lines += process_fillintheblank(line, dirname, args)
  shaded_block_lines += [
    "    \\end{shaded}\n",
    "\n",
    "\n"
      ]
  return shaded_block_lines

def process_fillintheblank(line, dirname, args):
  # parse numeric blank for student templates and put it in
  # as of 10/6/20: answerchoice, answernumeric
  line = strip_line(line)
  if line.startswith("\\answerchoice"):
    params = get_params(line)
    choice1, choice2 = params[:2]
    return [
      "    % bold your choice below\n",
      "    \\vspace*{2em} \\hspace*{0.5in}\n",
      "    {}     % to bold, \\textbf{{{}}}\n".format(choice1, choice1),
      "    \\hspace*{2pt} / \\hspace*{2pt}\n",
      "    {}     % to bold, \\textbf{{{}}}\n".format(choice2, choice2),
      "\n"
        ] + answer_block()
                  
  elif line.startswith("\\answernumeric"):
    params = get_params(line)
    units_str = params[1] # blankheight, units, postanswerheight
    return answer_block() + \
        [
"\n",  
"    \\begin{tabular}{l  p{.5in} p{2in} l}\n",
"    In addition to providing an expression above, \\\\\n",
"    please compute a numeric answer:&\n",
"    &           % replace with & 9999 (keeping ampersand (&) on left, 9999 being your answer)\n",
"    & {} \\\\\n".format(units_str),
"    \\cline{3-3}\n",
"    \\end{tabular}\n"
    ]
  elif line.startswith("\\answercoding"):
    params = get_params(line)
    blank_code_fname, soln_code_fname = params
    if not blank_code_fname.endswith(".tex"):
      blank_code_fname = "{}.tex".format(blank_code_fname)
    return read_template_lines(blank_code_fname, dirname, args) + ["\n"]
  elif line.startswith("\\answercodea"):
    # quiz 2 specific
    params = get_params(line)
    return answer_block() + \
        [
"\n",
"    \\begin{tabular}{p{1.6in} p{1.5in} b{.9in} p{1.5in}}\n",
"    \\multicolumn{4}{l}{In addition to providing justification above, please compute numeric answers:} \\\\ \\\\\n",
"    Smallest \\texttt{flop} return: &\n",
"            % write your flop smallest return value here (replace line)\n",
"    & probability: &\n",
"    		% write your flop probability here (replace line)\n",
"    \\\\ \\cline{2-2} \\cline{4-4} \\\\\n",
"    Second smallest \\\\\n",
"    \\texttt{flop} return: &\n",
"            % write your flop second smallest return value here (replace line)\n",
"    & probability: &\n",
"    		% write your flop probability here (replace line)\n",
"    \\\\\n",
"    \\cline{2-2} \\cline{4-4}\n",
"    \\end{tabular}\n",
    ]
  elif line.startswith("\\answercodeb"):
    # quiz 2 specific
    params = get_params(line)
    return answer_block() + \
        [
"\n",  
"    \\begin{tabular}{l  p{1.7in} p{.1in} p{1.7in}}\n",
"    \\multirow{3}{2in}{In addition to providing justification above,\n",
"    please compute numeric answers:} \\\\ \\\\\n",
"    &  \\texttt{flip}:\n",
"    			% write your flip answer here (replace line)\n",
"    & &  \\texttt{flop}:\n",
"    			% write your flop answer here (replace line)\n",
"    \\\\\n",
"    \\cline{2-2}\n",
"    \\cline{4-4}\n",
"    \\end{tabular}\n"
    ]
  elif line.startswith("\\answerpredict"):
    # quiz 3 specific
    params = get_params(line)
    return answer_block() + \
        [
"\n",
"    Your prediction: \\hspace*{0.1in}\n",
"    $\\hat{Y} = 0$ % to underline, \\underline{$\\hat{Y} = 0$}\n",
"    \\hspace*{2pt} / \n",
"    $\\hat{Y} = 1$ % to underline, \\underline{$\\hat{Y} = 1$}\n"
        ]

  else:
    return answer_block()

def answer_block():
  return [
    "    \\begin{answer}\n",
    "\n",
    "       % your answer here\n",
    "\n",
    "    \\end{answer}\n",
      ]

def shaded_answer_block(line, dirname, args):
  # for \answerspace, \answernumeric, \answerchoice, the last param
  # is always the solution file
  soln_fname = get_params(line)[-1]
  if not soln_fname.endswith(".tex"):
    soln_fname = "{}.tex".format(soln_fname)

  return [
    "    \\begin{shaded}\n",
    "    \\begin{answer}\n",
    "\n"] + \
        read_template_lines(soln_fname, dirname, args) + \
        [
    "\n",
    "    \\end{answer}\n",
    "    \\end{shaded}\n",
      ]

def blank_answer_block(line, dirname, args):
  line = strip_line(line)
  if line.startswith("\\answercoding"):
    # need to explicitly load in the file
    code_fname = get_params(line)[0]
    if not code_fname.endswith(".tex"):
      code_fname = "{}.tex".format(code_fname)

    return read_template_lines(code_fname, dirname, args)
  else:
    return [line] # otherwise, definition fully internal


def get_params(line):
  regex = r"\{(.*?)\}"
  params = re.findall(regex, line)
  return params

def placeholder_soln_lines():
  return [
   "    \\newcommand{\problempagebreak}[1]{}\n"
      ]
