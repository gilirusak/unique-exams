#!/usr/bin/python

''' Description: generates latex for unique quiz 2, cs109 spring 2020
    Author: Gili Rusak May 20, 2020
    Input:  i (number from 1-M); unique_rule.csv (MxN), where M = number of students, N = number of random numbers in exam
    Output: write find&replace unique exam to  tex/cs109_quiz02_i.tex
'''
import argparse
import csv
from itertools import product 
import numpy as np
import sys, getopt
import os
from numpy import genfromtxt

from scripts.config import *
from scripts.util.latex import read_template

parser = argparse.ArgumentParser(description="Generates LaTeX documents.")
parser.add_argument("quiz_number", type=int,
                    help="Quiz number to generate")
parser.add_argument("--soln", dest="is_soln", action="store_true",
                    help="Flag for creating solution document")
parser.add_argument("--template", dest="is_template", action="store_true",
                    help="Flag for creating template document")
args = parser.parse_args()

def get_template():
  if args.is_soln:
    return EXAM_SOLN_TEMPLATE
  return EXAM_TEMPLATE

def load_permutations_file():
  # get unique numbers for student number quiz_number
  with open(QUIZ_RULE_PERMUTATIONS_CSV, 'r', encoding="utf8") as f:
    rules_array = genfromtxt(['\t'.join(tup) \
                      for tup in csv.reader(f, delimiter=',', quotechar='"')],
                             delimiter='\t',
                             dtype=str)

  # return header and student rows
  return rules_array[0,:], rules_array[1:]

def prepare_headers():
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

def prepare_exam_path(quiz_id):
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

  if not os.path.exists(exam_dir):
    os.makedirs(exam_dir)

  exam_path = os.path.join(exam_dir, "{}.tex".format(exam_name))
  return exam_path

def get_quiz_rule(quiz_number):
  # safety checks
  assert(quiz_number >= 0 and quiz_number < TOTAL_NUM_QUIZZES)

  # row 1 is default quiz with index 0
  _, rules_array = load_permutations_file()

  unique_rule = rules_array[quiz_number]
  return unique_rule

def get_examid_key():
  if args.is_template:
    return "\\EXAMID"
  else:
    return "EXAMID_VALUE"

def main():
  quiz_number = args.quiz_number          # get exam number
  quiz_id = str(quiz_number).zfill(4)     # generate quiz id

  headers = prepare_headers()

  unique_rule = get_quiz_rule(quiz_number)
  assert(len(unique_rule) == len(headers))

  # read tex template
  template = read_template(get_template(), TEMPLATE_PATH_DIR, args)

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
  magic_template = magic_template.replace(get_examid_key(), quiz_id, 1)

  # write new tex file
  exam_path = prepare_exam_path(quiz_id)
  with open(exam_path, 'w') as writer:
    writer.write(magic_template)
    print("written to", writer.name)

if __name__ == '__main__':
  main()
