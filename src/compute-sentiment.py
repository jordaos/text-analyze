import sys
import sqlite3
import re
import os
from classes.cd import cd
from subprocess import call

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')

def compute_sentiments(conn, PATH):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM commits;")
  commits = cursor.fetchall()

  file_path = "%s/commits.txt" % (PATH)
  file = open(file_path, "w")
  for linha in commits:
    file.write(re.sub('\s+',' ', linha[1]) + '\n')
  file.close()

  with cd("tools/sentistrength"):
    call(["java", "-jar", "sentistrength-0.1.jar", "sentidata", "sentistrength_data/", "input", "../../" + file_path, "explain"])
  os.remove(file_path)

def put_in_sqlite(conn, PATH):
  conn.execute('DROP TABLE IF EXISTS sentiment;')
  conn.execute('''
      CREATE TABLE IF NOT EXISTS `sentiment` (
        `sha` TEXT, 
        `Positive` INTEGER, 
        `Negative` INTEGER, 
        `Text` TEXT, 
        `Explanation` TEXT )
    ''')
  
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM commits;")
  commits = cursor.fetchall()

  file_explanation_path = "%s/commits0_out.txt" % (PATH)
  file_explanation = open(file_explanation_path, "r")
  commit_analysis = file_explanation.readline()

  for linha in commits:
    commit_analysis = file_explanation.readline()
    arr_analysis = re.split(r'\t+', commit_analysis)

    cursor.execute("""
        INSERT INTO sentiment (sha, Positive, Negative, Text, Explanation)
        VALUES (?, ?, ?, ?, ?)
      """, (linha[0], arr_analysis[0], arr_analysis[1], linha[1], arr_analysis[3]))
  os.remove(file_explanation_path)


def main(argv):
  PROJECT_NAME = argv[1]
  PATH = 'data/%s' % PROJECT_NAME
  conn = sqlite3.connect('%s/DB/%s.sqlite' % (PATH, PROJECT_NAME))
  conn.text_factory = str
  compute_sentiments(conn, PATH)
  put_in_sqlite(conn, PATH)

  conn.commit()
  conn.close()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print 'Give parameter (project name)'
    sys.exit()
  main(sys.argv)