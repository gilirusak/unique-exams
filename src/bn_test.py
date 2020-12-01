DPROB = 0.3
DZEROLAMBA = 5
DONELAMBA = 8
DZEROLAMBB = 3
DONELAMBB = 6
VISITORSTOTAL = 12
		
import numpy as np
from scipy import stats
		
def infer_prob_total(total, ntrials):		
  n_samples_event = 0
  for i in range(ntrials):
    d = stats.bernoulli.rvs(DPROB)
    user_sum = 0			
    if d == 0:
      user_sum += stats.poisson.rvs(DZEROLAMBA) + stats.poisson.rvs(DZEROLAMBB)
    else:
      user_sum += stats.poisson.rvs(DONELAMBA) + stats.poisson.rvs(DONELAMBB)
		
    if user_sum == VISITORSTOTAL:
      n_samples_event += 1
		
  prob = n_samples_event/ntrials
  return prob

ntrials = 50000
total = 12
print("Simulated P(A + B)=", infer_prob_total(total, ntrials))
