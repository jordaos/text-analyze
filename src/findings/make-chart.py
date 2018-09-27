import statistics
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import sqlite3
matplotlib.use('Agg')

conn = None

def get_mean(score):
  sql = ""
  cursor = conn.cursor()
  cursor1.execute("SELECT * FROM findings;")

def main(argv):
  PROJECT_NAME = argv[1]
  PATH = 'data/%s' % PROJECT_NAME
  conn = create_db(PATH, PROJECT_NAME)
  x = np.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])
  y = np.power(x, 2) # Effectively y = x**2
  e = np.array([1.5, 2.6, 3.7, 4.6, 5.5])

  plt.errorbar(x, y, e, linestyle='None', marker='^')

  plt.show()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print 'Give parameter (project name)'
    sys.exit()
  main(sys.argv)