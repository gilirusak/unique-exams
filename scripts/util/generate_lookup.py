import csv
import numpy as np
import os

from scripts.config import *

ROSTER_FPATH = "../2020-11-03-roster.csv"
STUDENT_LOOKUP = "student_lookup.csv"
CGI_LOOKUP = "{}_lookup.csv".format(EXAM_NAME)

np.random.seed(1234)

student_lookup = {}
with open(ROSTER_FPATH, 'r') as f:
  reader = csv.reader(f)
  header = next(reader)
  for row in reader:
    student_name, _, _, sunetid, _, sid = row[:6]
    if int(sid) == 0:       # auditor, skip
      continue
    if len(row) > 6 and int(row[6]) > 0:
      # assuming the next column is withdraw, if any
      continue  
    student_lookup[sid] = [sid, sunetid, student_name]

sids = list(student_lookup.keys())
np.random.shuffle(sids)

all_rows = []
with open(QUIZ_RULE_PERMUTATIONS_CSV, 'r') as f:
  reader = csv.reader(f)
  header_param = next(reader)

  quiz_id = str(0).zfill(4)
  row = next(reader)
  all_rows.append(["0", "0", "Default", quiz_id] + row)
  for i, row in enumerate(reader):
    quiz_number = i + 1         # zero already used for default
    quiz_id = str(quiz_number).zfill(4)
    if i < len(sids):
      sid, sunetid, student_name = student_lookup[sids[i]]
      all_rows.append([sid, sunetid, student_name, quiz_id] + row)
    else:
      all_rows.append(["-1", "-1", "Blank", quiz_id] + row)

print("# students", len(student_lookup))
print("# exams", len(all_rows))

# write unique_rules with lookup
header_full = ["Student ID", "SUNetID", "Name", "Quiz ID"] + \
              header_param
with open(STUDENT_LOOKUP, 'w') as f:
  writer = csv.writer(f)
  writer.writerow(header_full)
  writer.writerows(all_rows)
  print("Google Sheets lookup written to", f.name)

# write lookup filename
# ignore zero-th row
cgi_rows = [(sunetid, "{}.zip".format(quiz_id)) \
          for _, sunetid, _, quiz_id, *_ in all_rows[1:]]
with open(CGI_LOOKUP, 'w') as f:
  writer = csv.writer(f)
  writer.writerows(cgi_rows)
  print("cgi-bin lookup written to", f.name)
