import copy
import cexprtk
import csv
import os

from scripts.config import FUNC_MAP

FIELDNAMES = [
    "VARNAME",
    "PROBLEM",
    "VARIABILITY",     # should be int
    "VARSYNC",         # should be a VARNAME (str)
    "SOLN",            # should be 1 or 0 or blank string
    "FUNCTION"
    # "VALUES"         # will be auto-generated from restkey
    ]

def load_variables_file(fpath):
  """
  Each row is a dictionary with values as specified in FIELDNAMES
  """
  print(os.getcwd())
  reader = csv.DictReader(open(fpath, encoding='utf-8-sig'),
                          fieldnames=FIELDNAMES,
                          restkey='VALUES')
  new_reader = []
  for row in reader:
    # update values to remove any blank fields
    if 'VALUES' in row:
      row['VALUES'] = process_values(row['VALUES'])
    if 'SOLN' in row:
      row['SOLN'] = process_soln(row['SOLN'])
    new_reader.append(row)
  return new_reader

def process_soln(soln_int):
  try:
    return int(soln_int) == 1
  except:
    return False

def process_values(row):
  new_row = []
  for item in row:
    if not len(item): continue
    try: # if not int,
      new_row.append(int(item))
    except ValueError:
      try:
        new_row.append(float(item))
      except ValueError:
        new_row.append(str(item))
  return new_row

def get_problems(reader):
  problems = set([row['PROBLEM'] for row in reader])
  return list(problems)

def get_independent_vars(reader, problem):
  # return all variables with PROBLEM=problem
  # that don't have VARSYNC or FUNCTION set
  # TODO: return in order of variability (or default)
  problem_reader = []
  for row in reader:
    if row['PROBLEM'] != problem:
      continue
    if len(row['VARSYNC']):
      continue
    if len(row['FUNCTION']):
      continue
    problem_reader.append(row)
    
  return problem_reader

def get_function_vars(reader, problem):
  """
  Do not return constraints (see get_constraint_vars())
  """
  problem_reader = []
  for row in reader:
    if row['PROBLEM'] != problem:
      continue
    if len(row['FUNCTION']) and len(row['VARNAME']):
      problem_reader.append(row)
  return problem_reader

def get_constraints(reader, problem):
  """
  Constraints have a function field but do not define a new variable.
  """
  problem_reader = []
  for row in reader:
    if row['PROBLEM'] != problem:
      continue
    if len(row['FUNCTION']) and len(row['VARNAME']) == 0:
      problem_reader.append(row)
  return problem_reader


def get_synced_vars(reader, problem):
  problem_reader = []
  for row in reader:
    if row['PROBLEM'] != problem:
      continue
    if len(row['VARSYNC']):
      problem_reader.append(row)
  return problem_reader

##################################### permutation functionality
def make_vars(tups):
  """
  Map varname -> value
  """
  return dict([(varname, value) for varname, value in tups])

def get_sync_tup(row, var_dict, indep_dict, sync_dict):
  varsync = row['VARSYNC']

  assert(varsync in var_dict) # specified variable must be one of the varied
  indep_value = var_dict[varsync]

  if varsync in indep_dict:
    possible_indep_values = indep_dict[varsync]
  elif varsync in sync_dict:
    possible_indep_values = sync_dict[varsync]
  sync_values = row['VALUES']
  value = sync_values[possible_indep_values.index(indep_value)]
  return row['VARNAME'], value

def get_func_tup(row, symtab):
  value = evaluate_expression(row['FUNCTION'], symtab)
  return row['VARNAME'], value
  
def evaluate_constraint(row, symtab):
  return evaluate_expression(row['FUNCTION'], symtab)

################################ symbol table wrapper for cexprtk
def make_symtab(var_dict):
  """
  Make a cexprtk Symbol Table from the provided (varname, value) dictionary.

  Also add in any functions that reference external libraries.
  Note that cexprtk doesn't accept any import commands, so you'll have to
  custom define the functions.
  """
  symtab = cexprtk.Symbol_Table(var_dict)
  update_symtab_functions(symtab)
  return symtab

def update_symtab_var(symtab, varname, value):
  symtab.variables[varname] = value

def update_symtab_functions(symtab):
  """
  CUSTOM FUNCTION that you must write 
  """
  for k, v in FUNC_MAP.items():     # defined in config.py
    symtab.functions[k] = v

def evaluate_expression(func_str, symtab):
  expression = cexprtk.Expression(func_str, symtab)
  return expression()
