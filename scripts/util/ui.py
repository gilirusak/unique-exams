import operator
"""
User Interface written by the wonderful Julie Zelenski
(zelenski@cs.stanford.edu) and ported over to Python3 by Lisa Yan
(yanlisa@stanford.edu)
"""

def get_choice(prompt, options,
      default=None, allow_comment=False, cmp=operator.contains):
  """
  The mother of all input routines.  Client lists valid options. Will prompt 
  user to enter response, returns choice if valid (e.g. appears in list of 
  options), otherwise retry. The options in list can be strings/numbers (or 
  anything for which str() works). If there is a default, it will be used 
  when user enters empty string.  If allow_comment is True, will parse first 
  token as choice and return tuple (choice, rest of line). Default match 
  operation is contains (i.e. substring match). use operator.eq for equality 
  or str.startswith for prefix match
  """
  if default:
    offer = " [%s]:" % default
  elif len(options) == 2:
    offer = " [%s]:" % '/'.join([str(o) for o in options])
  else:   
    offer = " "
  while True:
    response = get_input(prompt + offer)
    if response == "":
      if default: 
        choice,comment = (default, "")
        break
    else:       
      tokens = response.split()
      choice,comment = (tokens[0], ' '.join(tokens[1:]))
      choice = unique_match(choice, options, cmp)
      if choice is not None: break
      print("Try again. Options are %s" % pretty_list(options))
  return (choice, comment) if allow_comment else choice

def get_yes_or_no(prompt, default=None):
  return get_choice(prompt, ["y", "n"],
                      default=default, allow_comment=False) == "y"

def unique_match(pattern_str, choices, cmp=operator.contains):
    """
    looks for a pattern_str in a list of choices (each choice converted to str 
    for cmp). default cmp allows substring match, use operator.eq for equality 
    or str.startswith for prefix match"""
    if pattern_str in choices:
      # exact match, return that one without looking further
      return pattern_str  

    # gather matches (prefix/substr/etc)
    matches = [c for c in choices if cmp(str(c), pattern_str)]  
    return matches[0] if len(matches) == 1 else None  # return if unique


def pretty_list(list, maxitems=-1):
  """
  Calls str on each item to get more human-readable form, by default no abbreviate
  """
  if maxitems != -1 and len(list) > maxitems:
    list = list[0:maxitems] + ["..."]
  # recognizes list that represents range and reports as such
  if len(list) >= 2 and isinstance(list[0], int) and isinstance(list[-1], int) and list == range(list[0], list[-1]+1):
    return "[%s to %s]" % (list[0], list[-1])
  return "[%s]" % (", ".join((str(item) for item in list)))


def get_input(prompt):
  try:
    return input(prompt).strip()
  except (EOFError, KeyboardInterrupt):
    # EOF will result if user entered Ctrl-D or stdin pipe hit dead end
    # re-map to Ctrl-C (interrupt) and hook will handle as user cancel/interrupt
    print()  # print CR to advance output beyond prompt to next line for any message printed
    raise KeyboardInterrupt
