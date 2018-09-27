import sqlite3
import sys
from classes.cd import cd
import subprocess

def change_db(conn):
  cursor = conn.cursor()
  column1 = "ALTER TABLE commits ADD insertions INTEGER NULL"
  column2 = "ALTER TABLE commits ADD deletions INTEGER NULL"
  cursor.execute(column1)
  cursor.execute(column2)
  cursor.close()

def add_count(REPO_PATH, conn):
  sql = "SELECT * FROM commits;"
  cursor = conn.cursor()
  cursor.execute(sql)
  commits = cursor.fetchall()
  for commit in commits:
    sha = commit[0]
    with cd(REPO_PATH):
      lines = subprocess.check_output(
        ['git', 'log', '--oneline', '--stat', sha, '-1'], stderr=subprocess.STDOUT
      ).split('\n')
      penul = len(lines) - 2
      penul_line = lines[penul]
      if 'changed' in penul_line:
        insertions = 0
        deletions = 0
        if 'insertion' in penul_line:
          inser_arr = penul_line.split('insertion')
          part_1 = inser_arr[0]
          comma_arr = part_1.split(',')
          part_2 = comma_arr[1]
          insertions = int(part_2)
        
        if 'insertion' in penul_line and 'deletion' in penul_line:
          inser_arr = penul_line.split('deletion')
          part_1 = inser_arr[0]
          comma_arr = part_1.split(',')
          part_2 = comma_arr[2]
          deletions = int(part_2)
        elif 'deletion' in penul_line:
          inser_arr = penul_line.split('deletion')
          part_1 = inser_arr[0]
          comma_arr = part_1.split(',')
          part_2 = comma_arr[1]
          deletions = int(part_2)

        update_sql = 'UPDATE commits SET insertions = ?, deletions = ? WHERE sha = ?'
        cursor.execute(update_sql, (insertions, deletions, sha))
  cursor.close()

def main(argv):
  PROJECT_NAME = argv[1]
  PATH = 'data/%s' % PROJECT_NAME
  REPO_PATH = '%s/Repository/%s' % (PATH, PROJECT_NAME)
  conn = sqlite3.connect('%s/DB/%s.sqlite' % (PATH, PROJECT_NAME))
  change_db(conn)

  add_count(REPO_PATH, conn)

  conn.commit()
  conn.close()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print('Give parameter (project name)')
    sys.exit()
  main(sys.argv)