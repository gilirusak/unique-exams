#!/usr/bin/python
"""
Author: yanlisa@stanford.edu

Use Student ID number to add two columns to lookup CSV:
  - Submission ID
  - Submission Time
  - If these fields don't exist, the student hasn't submitted yet. Leave empty.

Then upload to Google Sheets and sort.

Order:
  - Gradescope submission time (note only accurate to the minute, so the order
    of Gradescope CSV needs to be preserved)
"""
import csv
import numpy as np
import os

from config import *

GRADESCOPE_CSV = "../Quiz_2_scores.csv"
STUDENT_LOOKUP = "student_lookup.csv"
SUBMISSION_CSV = "submission_lookup.csv"

row_lookup = {}
extra_rows = []
with open(STUDENT_LOOKUP, 'r') as f:
  reader = csv.reader(f)
  header = next(reader)
  header_sid, header_quizid, header_name = header[:3]
  header_fields = header[3:]
  for row in reader:
    sid = int(row[0])         # strip leading zeros
    student_name = row[2]
    if sid not in row_lookup:
      row_lookup[sid] = row
    else:
      extra_rows.append(row)

all_rows = []
unused_exams = set(row_lookup.keys())
with open(GRADESCOPE_CSV, 'r') as f:
  reader = csv.reader(f)
  header = next(reader)
  for row in reader:
    submission_status = row[header.index("Status")]
    if submission_status == "Missing":
      continue

    student_name, sid, email = row[:3]
    sid = int(sid)              # strip leading zeros
    submission_id = row[header.index("Submission ID")]
    submission_time = row[header.index("Submission Time")]
    assert(len(submission_id))  # should always pass for non-missing submissions

    if sid not in row_lookup:
      print("Alert!", sid, "in Gradescope but does not have a personalized exam.")
      print("   Using default exam.")
      # rewrite with correct with student_name, sid, email (in that order)
      student_name = row[header.index("Name")]
      email = row[header.index("Email")]
      sunetid = email.split('@')[0]
      row = row_lookup[0]
    else:
      row = row_lookup[sid]
      unused_exams.remove(sid)
      sid, sunetid, student_name = row[:3]

    all_rows.append([sid, sunetid, student_name, submission_id, submission_time] + row[3:])

for unused_sid in unused_exams:
  print("unused sid", unused_sid)
  submission_id, submission_time = "", ""
  row = row_lookup[unused_sid]
  all_rows.append(row[:3] + [submission_id, submission_time] + row[3:])

for extra_row in extra_rows:
  submission_id, submission_time = "", ""
  all_rows.append(extra_row[:3] + [submission_id, submission_time] + extra_row[3:])

headers = [header_sid, header_quizid, header_name, "Submission ID", "Submission Time"] + \
          header_fields

with open(SUBMISSION_CSV, 'w') as f:
  writer = csv.writer(f)
  writer.writerow(headers)
  writer.writerows(all_rows)
