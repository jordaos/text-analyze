import statistics
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import sqlite3
import sys

conn = sqlite3.connect('data/all.sqlite')

def dp(score):
  sql = '''
    SELECT (F.resolved / (cast((F.unresolved + F.resolved) as FLOAT))) FROM findings F 
      INNER JOIN sentiment S ON S.sha = F.sha
      WHERE (S.positive + S.negative) = ? AND
      (F.unresolved + F.resolved) > 0 AND
      (S.Positive <> 1 OR S.Negative <> -1) AND
      F.sha <> 'b49c1296eb569afcaee5b521ad2d0c7afd921d8f';
  '''
  cursor = conn.cursor()
  cursor.execute(sql, (score,))
  commits = cursor.fetchall()
  values = [commit[0] for commit in commits]
  if len(values) <= 1: return 0
  dp = statistics.stdev(values)
  dpma = (dp / (len(values) ** 0.5)) # desvio padrao da media amostral
  return dpma

def mean(score):
  sql = '''
    SELECT AVG(F.resolved / (cast((F.unresolved + F.resolved) as FLOAT))) FROM findings F
      INNER JOIN sentiment S ON S.sha = F.sha
      WHERE (S.positive + S.negative) = ? AND
      (F.unresolved + F.resolved) > 0 AND 
      (S.Positive <> 1 OR S.Negative <> -1) AND
      F.sha <> 'b49c1296eb569afcaee5b521ad2d0c7afd921d8f';
  '''
  cursor = conn.cursor()
  cursor.execute(sql, (score,))
  mean = cursor.fetchone()
  if mean[0] == None: return 0
  return mean[0]

def main():
  x = np.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])

  # DPs
  m4 = dp(-4)
  m3 = dp(-3)
  m2 = dp(-2)
  m1 = dp(-1)
  z = dp(0)
  p1 = dp(1)
  p2 = dp(2)
  p3 = dp(3)
  p4 = dp(4)

  # means
  meanm4 = mean(-4)
  meanm3 = mean(-3)
  meanm2 = mean(-2)
  meanm1 = mean(-1)
  mean0 = mean(0)
  meanp1 = mean(1)
  meanp2 = mean(2)
  meanp3 = mean(3)
  meanp4 = mean(4)

  e = np.array([m4, m3, m2, m1, z, p1, p2, p3, p4])
  y = np.array([meanm4, meanm3, meanm2, meanm1, mean0, meanp1, meanp2, meanp3, meanp4])

  print("e")
  print(e)
  print("-----------")
  print("y")
  print(y)

  plt.errorbar(x, y, e, linestyle='None', marker='^')
  plt.show()

if __name__ == "__main__":
  main()