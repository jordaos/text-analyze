import statistics
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import sqlite3
import sys

conn = sqlite3.connect('data/all.sqlite')

def dp(score):
  sql = '''
    SELECT (C.insertions / F.new) FROM findings F 
      INNER JOIN commits C ON C.sha = F.sha
      INNER JOIN sentiment S ON S.sha = F.sha
      WHERE (S.positive + S.negative) = ? AND
      F.new > 0 AND 
      C.insertions IS NOT NULL AND
      (S.Positive <> 1 OR S.Negative <> -1);
  '''
  cursor = conn.cursor()
  cursor.execute(sql, (score,))
  commits = cursor.fetchall()
  print("%s - len = %s" % (score, len(commits)))
  values = [commit[0] for commit in commits]
  if len(values) == 0: return 0
  dp = statistics.pstdev(values)
  return dp

def main():

  x = np.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])
  y = np.array([9.5, 15.5454545454545, 32.9561403508772, 38.7198203256597, 32.3438438438438, 26.6976047904192, 27.0948275862069, 6.0, 0])

  # DPs
  m4 = dp(-4)
  m3 = dp(-3)
  m2 = dp(-2)
  m1 = dp(-1)
  z = dp(0)
  p1 = int(dp(1))
  p2 = dp(2)
  p3 = dp(3)
  p4 = dp(4)

  e = np.array([m4, m3, m2, m1, z, p1, p2, p3, p4])
  print(x)
  print(y)
  print(e)

  plt.errorbar(x, y, e, linestyle='None', marker='^')
  plt.show()

if __name__ == "__main__":
  main()