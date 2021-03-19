"""
This file should be populated with functions that you'd like
to use in variables.csv.
"""
import fractions
import itertools
from util.header import *      # also sets seed
from scipy import stats, special

############################ step 1 ###############################
# define any additional helper functions here.
def dummy(varc, vard):
  # dummy function to edit
  return "test"

def phi(value):
  return stats.norm.cdf(value)

def pdf_constant(cx, cy, xbound, ybound):
  return fractions.Fraction(6, 
      2 * cx * (xbound ** 3) * ybound + 3 * cy * (ybound ** 2) * xbound)

def expectation_y(cx, cy, xbound, ybound, cnum, cdenom):
  #round(CONST*((XVAR*(XBOUND ** 3)*(YBOUND ** 2))/6 + (YVAR*XBOUND*(YBOUND ** 3))/3), 4)
  ey = fractions.Fraction(cx * (xbound ** 3) * (ybound ** 2) , 6)
  ey += fractions.Fraction(cy * xbound * (ybound ** 3), 3)
  ey = ey * fractions.Fraction(cnum, cdenom)
  return ey

def mystery(n, vara, varb, varc):
  # the code problem in python format
  # since the C function was for unsigned chars, the 32-bit int
  # arithmetic right shift is sufficient for the parameters given
  n = n | (n >> vara)
  n = n | (n >> varb)
  n = n | (n >> varc)
  n = (n + 1) & 0xff # char byte
  return (n >> 1) & 0xff # char byte


############################ step 2 ###############################
# functions that you call in variables.csv. Must be associated
# with real python functions, otherwise you should define them.
# needed especially if you use any packages.

FUNC_MAP = {
      "poisson_pmf": stats.poisson.pmf,
      "binom_pmf": stats.binom.pmf,
      "norm_pdf": stats.norm.pdf,
      "binom": special.binom,
      "dummy": dummy,
      "phi": phi,
      "pdf_constant": pdf_constant,
      "expectation_y": expectation_y,
      "mystery": mystery,
    }
