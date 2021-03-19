from config import *

def lookup_main():
  student_lookup = {}
  with open(ROSTER_FPATH, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    sid_ind = header.index("ID")
    email_ind = header.index("Email")
    name_ind = header.index("Name")
    for row in reader:
      sid = row[sid_ind]
      if int(sid) == 0:       # auditor, skip
        continue
      student_lookup[sid] = [sid, row[email_ind], row[name_ind]]
  
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
        sid, email, student_name = student_lookup[sids[i]]
        all_rows.append([sid, email, student_name, quiz_id] + row)
      else:
        all_rows.append(["-1", "-1", "Blank", quiz_id] + row)
  
  print("# students", len(student_lookup))
  print("# exams", len(all_rows))
  
  # write unique_rules with lookup
  header_full = ["ID", "Email", "Name", "Quiz ID"] + \
                header_param
  with open(STUDENT_LOOKUP, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header_full)
    writer.writerows(all_rows)
    print("CSV lookup written to", f.name)
