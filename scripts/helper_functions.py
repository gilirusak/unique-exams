import itertools
import numpy as np
import os
from scipy import stats, special

np.random.seed(1234)     # deterministic

# write any additional helper functions here.
def cast_int(value):
  return int(value)

def cast_float(value):
  return float(value)

def dummy(varc, vard):
  # dummy function to edit
  return "test"

def phi(value):
  return stats.norm.cdf(value)

def right_bitshift(value, shift):
  return value >> shift

def pipe(value1, value2):
  return int(value1) | int(value2)

# Generates unique numbers for problem 1
# This is the full-time jobs question
def bernoulli_rules():
  header = [
      # indep params
      "STANFORDRATE", "BERKELEYRATE", "STANFORDRATECOMP", "BERKELEYRATECOMP", "NTRIALS", "NSUCCESSES",
      "SAMPLESIZE", "THRESHOLD",
      # solutions
      "BERNOULLISOLNA", "BERNOULLISOLNB", "BERNOULLISOLNCPROBBOTHBERKWORK", "BERNOULLISOLNCPROBBOTHWORK", "BERNOULLISOLNCWITHOUT", "BERNOULLISOLNCWITH", "NORMALMEAN", "NORMALVAR", "NORMALSTD", "THRESHOLDCC", "NORMALZ", "BERNOULLISOLND"
      ]
  # indep variables for problem 1
  STANFORDRATE = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81]
  BERKELEYRATE = [59, 60, 61, 82, 83, 84, 85, 86, 87, 88, 89, 90] # don't include 91 or higher so that all numbers are two digits
  NTRIALS = [12, 13, 14, 15, 16, 17, 18, 19, 20] # don't couple with above two
  SUCCESS_DIFF = [-1, 0, 1, 2, 3, 4]
  SAMPLESIZE = 120
  NUMSTANFORDSTUDENTS = 7000
  NUMBERKELEYSTUDENTS = 33000
  NUMSTUDENTS = NUMSTANFORDSTUDENTS + NUMBERKELEYSTUDENTS
  PROBFARM = NUMSTANFORDSTUDENTS / NUMSTUDENTS
  PROBUCB = NUMBERKELEYSTUDENTS / NUMSTUDENTS
  
  unique_rules = itertools.product(STANFORDRATE, BERKELEYRATE)
  valid_rules = []

  for rule in unique_rules:
    rule = list(rule)
    stanfordrate, berkeleyrate = rule
    
    # functions
    stanfordratecomp, berkeleyratecomp = 100 - stanfordrate, 100 - berkeleyrate
    rule += [ stanfordratecomp, berkeleyratecomp ]
    sp, bp, sq, bq = stanfordrate/100, berkeleyrate/100, stanfordratecomp/100, berkeleyratecomp/100

    # a

    # b
    ntrials = np.random.choice(NTRIALS);
    nsuccesses = ntrials // 2 + np.random.choice(SUCCESS_DIFF)
    assert(nsuccesses < ntrials)
    rule += [ntrials, nsuccesses]
    
    # c
    #bp = 0.61
    #sp = 0.65
    # prob of work, work given berk, berk
    pwwbb = bp * bp
    # prob of selecting two berkeley students with and without replacement
    pbbwith = (NUMBERKELEYSTUDENTS / NUMSTUDENTS) * (NUMBERKELEYSTUDENTS / NUMSTUDENTS)
    pbbwithout = (NUMBERKELEYSTUDENTS / NUMSTUDENTS) * ((NUMBERKELEYSTUDENTS - 1) / (NUMSTUDENTS - 1))
    pwwbs = bp * sp
    pbswith = (NUMBERKELEYSTUDENTS / NUMSTUDENTS) * (NUMSTANFORDSTUDENTS / NUMSTUDENTS)
    pbswithout = (NUMBERKELEYSTUDENTS / NUMSTUDENTS) * (NUMSTANFORDSTUDENTS / (NUMSTUDENTS - 1))
    pwwss = sp * sp
    psswith = (NUMSTANFORDSTUDENTS / NUMSTUDENTS) * (NUMSTANFORDSTUDENTS / NUMSTUDENTS)
    psswithout = (NUMSTANFORDSTUDENTS / NUMSTUDENTS) * ((NUMSTANFORDSTUDENTS - 1) / (NUMSTUDENTS - 1))
    # what's wrong with these two lines below
    pwwwith =    pwwbb * pbbwith +    2 * pwwbs * pbswith    + pwwss * psswith
    pwwwithout = pwwbb * pbbwithout + 2 * pwwbs * pbswithout + pwwss * psswithout
    pbbwwwith = pwwbb * pbbwith / pwwwith
    pbbwwwithout = pwwbb * pbbwithout / pwwwithout
    #print(pwwwith, pwwwithout)
    #x = crash + 1
    
    # d
    ssize = SAMPLESIZE + 10 * stanfordratecomp + berkeleyratecomp # hack to generate unique values based on original rule
    ssize -= ssize % 10
    mean = ssize * sp
    variance = ssize * sp * sq
    std = variance ** 0.5
    nstdsbelow = stanfordratecomp / berkeleyratecomp / 4 # hack, but deterministic hack
    threshold = int(mean - nstdsbelow * std)
    threshold -= threshold % 10
    rule += [ssize, threshold]
    thresholdcc = threshold + 0.5
    z = (mean - thresholdcc) / std
    assert(z <= 2.0)
    assert(z >= 0)
    assert(stats.norm.cdf(0) == 0.5)

    # solutions
    solution_a = special.binom(5, 4) * sp ** 4 * sq ** 1 * bp ** 5 + special.binom(5, 4) * sp ** 5 * bp ** 4 * bq ** 1
    assert(solution_a > 0 and solution_a < 1)
    solution_b = special.binom(ntrials - 1, nsuccesses - 1) * sp ** (nsuccesses) * sq ** (ntrials - nsuccesses)
    assert(solution_b > 0 and solution_b < 1)
    solution_c_pwwbb = pwwbb
    solution_c_pww = pwwwithout
    solution_c_without = pbbwwwithout
    solution_c_with = pbbwwwith
    assert(solution_c_without > 0 and solution_c_without < 1)
    assert(solution_c_with > 0 and solution_c_with < 1)
    solution_d = stats.norm.cdf(z)

    # rounding/casting
    solution_a = ("%.4f" % solution_a).rstrip('0')
    solution_b = ("%.4f" % solution_b).rstrip('0')
    solution_c_pwwbb = ("%.6f" % solution_c_pwwbb).rstrip('0')
    solution_c_pww = ("%.6f" % solution_c_pww).rstrip('0')
    solution_c_without = ("%.8f" % solution_c_without).rstrip('0')
    solution_c_with = ("%.8f" % solution_c_with).rstrip('0')
    mean = ("%.2f" % mean).rstrip('.0')
    std = ("%.2f" % std).rstrip('0')
    z = ("%.4f" % z).rstrip('0')
    variance = ("%.2f" % variance).rstrip('0')
    solution_d = ("%.4f" % solution_d).rstrip('0')

    rule += [solution_a, solution_b,
              solution_c_pwwbb, solution_c_pww, solution_c_without, solution_c_with,
              mean, variance, std, thresholdcc, z, solution_d]

    # convert to strings to avoid float/integer issues
    rule = [str(x) for x in rule]

    # conditions
    valid_rules.append(rule)
  
  return header, valid_rules
