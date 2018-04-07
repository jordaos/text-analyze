import sqlite3
import sys
import csv
from subprocess import check_output
from classes.cd import cd

def store_commits(REPO_PATH, LOG_FILE_PATH, conn):
  with open(LOG_FILE_PATH, "r") as lines:
    for line in lines.readlines():
      line = line.rstrip('\n')
      if ("No refactorings found in commit" in line):
        sha = line.split()[-1]
        commitMessage = ''
        with cd(REPO_PATH):
          commitMessage = check_output(['git', 'log', '--format=%B', '-n', '1', sha])
        rowsCommit = (sha, commitMessage)
        sqlInsertCommit = 'INSERT INTO commits VALUES(?, ?)'

        cursor = conn.cursor()
        cursor.execute(sqlInsertCommit, rowsCommit)
        cursor.close()

def main(argv):
  PROJECT_NAME = argv[1]
  PATH = 'data/%s' % PROJECT_NAME
  LOG_FILE_PATH = '%s/log.txt' % PATH
  REPO_PATH = '%s/Repository/%s' % (PATH, PROJECT_NAME)
  conn = sqlite3.connect('%s/DB/%s.sqlite' % (PATH, PROJECT_NAME))
  conn.text_factory = str

  store_commits(REPO_PATH, LOG_FILE_PATH, conn)

  conn.commit()
  conn.close()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print 'Give parameter (project name)'
    sys.exit()
  main(sys.argv)