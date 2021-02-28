"""
The general form of generate_permutations.py

Reads in from variables.csv and spits out a file of unique rules
"""
import fractions
import itertools

from config import *
from util.variables import *

def generate_rule_permutations(reader, problem):
  print(problem)
  # independent parameters for problem
  indep_params = get_independent_vars(reader, problem)
  indep_dict = dict([(row['VARNAME'], row['VALUES']) for row in indep_params])

  # synced variables (independent parameters)
  sync_params = get_synced_vars(reader, problem)
  sync_dict = dict([(row['VARNAME'], row['VALUES']) for row in sync_params])

  # functions (dependent parameters)
  func_params = get_function_vars(reader, problem)

  # finally, constraints (not added to header)
  constraints = get_constraints(reader, problem)

  header = organize_header(indep_params, sync_params, func_params)

  ## generate all rules
  # the order of indep_values
  indep_names = [row['VARNAME'] for row in indep_params]
  # the different values for each of the names in indep_names
  indep_values = [row['VALUES'] for row in indep_params]
  unique_rules = itertools.product(*indep_values)
  valid_rules = []

  for rule in unique_rules:
    rule = list(rule)
    indep_tups = zip(indep_names, rule)
    var_dict = make_vars(indep_tups)
    
    ## get sync params
    for row in sync_params:
      sync_name, sync_val = get_sync_tup(row, var_dict, indep_dict, sync_dict)
      var_dict[sync_name] = sync_val

    ## make functions
    # first create the cexprtk dictionary
    symtab = make_symtab(var_dict)

    for row in func_params:
      dep_name, dep_val = get_func_tup(row, symtab)
      var_dict[dep_name] = dep_val
      update_symtab_var(symtab, dep_name, dep_val)

    ## ignore invalid rows if constraints fail
    failed_constraint = False
    for row in constraints:
      # if a constraint fails, continue to the next row
      if not evaluate_constraint(row, symtab):
        failed_constraint = True
        break

    if failed_constraint:
      continue

    ## clean up and pretty print
    rule = var_dict_to_rule(var_dict, header)
    rule = round_rule(rule)
    rule = [str(x) for x in rule]

    valid_rules.append(rule)

  valid_rules = verify_rule_count(valid_rules, problem)
  return header, valid_rules

def organize_header(indep_params, sync_params, func_params):
  """
  Sort such that all problem variables are first and all solution
  variables follow.
  """
  all_params = indep_params + sync_params + func_params
  prob_headers, soln_headers = [], []
  for row in all_params:
    if row['SOLN']:
      soln_headers.append(row['VARNAME'])
    else:
      prob_headers.append(row['VARNAME'])
  print("prob", prob_headers)
  print("soln", soln_headers)
  return prob_headers + soln_headers

def var_dict_to_rule(var_dict, header):
  return [var_dict[varname] for varname in header]

def round_rule(rule):
  for i, value in enumerate(rule):
    if type(value) == int:
      continue
    elif type(value) == float:
      if value.is_integer():
        rule[i] = int(value) # always cast integers if you can
      else:
        rule[i] = ("%.5f" % value).rstrip('0.')
  return rule

def verify_rule_count(valid_rules, problem):
  if len(valid_rules) < TOTAL_NUM_QUIZZES:
    print("warning ({}): valid rules for loop is {}".format(
            problem, len(valid_rules)))
  else:
    print("OK ({}): valid rules for loop is {}".format(
            problem, len(valid_rules)))
  # repeat valid rules if not enough
  while len(valid_rules) < TOTAL_NUM_QUIZZES:
    valid_rules += valid_rules

  valid_rules_arr = np.array(valid_rules)
  valid_rules_arr = valid_rules_arr[:TOTAL_NUM_QUIZZES, :]
  return valid_rules_arr

def write_unique_rules(unique_rules, header, fname):
  with open(fname, 'w') as rules_file:
    rulewriter = csv.writer(rules_file)
    rulewriter.writerow(header)
    for row in unique_rules:
      rulewriter.writerow(row)
    print("wrote file", rules_file.name, "with", TOTAL_NUM_QUIZZES, "rows")

def permutations_main():
  vars_reader = load_variables_file(VARIABLES_FNAME)
  unique_rules = []
  header_all = []
  for problem in PROBLEMS:
    if problem in QUESTION_MAP:
      # problem has a hard-coded function associated with it
      header, valid_rules = QUESTION_MAP[problem]()
      unique_rules_problem = verify_rule_count(valid_rules, problem)
    else:
      header, unique_rules_problem = generate_rule_permutations(vars_reader, problem)
    unique_rules.append(unique_rules_problem)
    header_all += header

  unique_rules = np.concatenate(unique_rules, axis=1)
  assert(unique_rules.shape == (TOTAL_NUM_QUIZZES, len(header_all)))

  write_unique_rules(unique_rules, header_all, UNIQUE_RULES_FNAME)

if __name__ == '__main__':
  permutations_main()
