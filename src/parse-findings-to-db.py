import csv
import sqlite3
import sys

def getSha(littleSha, conn):
  like = littleSha + '%'
  cursor = conn.cursor()
  cursor.execute("SELECT sha FROM commits WHERE sha LIKE ?", [like])
  return cursor.fetchone()[0]

def insert(commit, conn):
  cursor = conn.cursor()
  commit[0] = getSha(commit[0], conn)
  sqlInsert = 'INSERT INTO findings VALUES(?,?,?,?)'
  cursor.execute(sqlInsert, commit)
  cursor.close()

def main(argv):
  PROJECT_NAME = argv[1]
  PATH = 'data/%s' % PROJECT_NAME
  FINDINGS_FILE = '%s/findings.csv' % PATH
  # DB
  conn = sqlite3.connect('%s/DB/%s.sqlite' % (PATH, PROJECT_NAME))
  conn.text_factory = str
  conn.execute('DROP TABLE IF EXISTS findings;')
  conn.execute('''
    CREATE TABLE IF NOT EXISTS `findings` (
      `sha` TEXT, 
      `new` INTEGER, 
      `unresolved` INTEGER,
      `resolved` INTEGER)
    ''')

  with open(FINDINGS_FILE) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
      sha = row[0]
      new = (row[1] if row[1] != '' else 0)
      unresolved = (row[2] if row[2] != '' else 0)
      resolved = (row[3] if row[3] != '' else 0)
      currentCommit = [sha, new, unresolved, resolved]
      insert(currentCommit, conn)
  
  conn.commit()
  conn.close()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print 'Give parameter (project name)'
    sys.exit()
  main(sys.argv)