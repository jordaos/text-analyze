import subprocess
import re
import sys
import sqlite3
from classes.cd import cd

leading_4_spaces = re.compile('^  ')

def get_commits(REPO_PATH, BRANCH):
  lines = ''
  with cd(REPO_PATH):
    lines = subprocess.check_output(
      ['git', 'log', BRANCH], stderr=subprocess.STDOUT
    ).split('\n')
  commits = []
  current_commit = {}

  def save_current_commit():
    message = current_commit.get("message", "")
    current_commit['message'] = '\n'.join(message)
    commits.append(current_commit)

  for line in lines:
    if not line.startswith(' '):
      if line.startswith('commit '):
        if current_commit:
          save_current_commit()
          current_commit = {}
        current_commit['hash'] = line.split('commit ')[1]
      else:
        try:
          key, value = line.split(':', 1)
          current_commit[key.lower()] = value.strip()
        except ValueError:
          pass
    else:
      current_commit.setdefault(
        'message', []
      ).append(leading_4_spaces.sub('', line))
  if current_commit:
    save_current_commit()
  return commits

def save(commits, conn):
  conn.execute('DROP TABLE IF EXISTS commits;')
  conn.execute('''
    CREATE TABLE IF NOT EXISTS `commits` (
      `sha` TEXT, 
      `message` TEXT, 
      `date` TEXT)
    ''')
  cursor = conn.cursor()

  sqlInsert = 'INSERT INTO commits VALUES(?, ?, ?)'
  for commit in commits:
    rows = (commit['hash'], commit['message'], commit['date'])
    cursor.execute(sqlInsert, rows)

def main(argv):
  PROJECT_NAME = argv[1]
  BRANCH = argv[2]
  PATH = 'data/%s' % PROJECT_NAME
  REPO_PATH = '%s/Repository/%s' % (PATH, PROJECT_NAME)
  # DB config
  conn = sqlite3.connect('%s/DB/%s.sqlite' % (PATH, PROJECT_NAME))
  conn.text_factory = str

  commits = get_commits(REPO_PATH, BRANCH)
  save(commits, conn)

  conn.commit()
  conn.close()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print('Give parameter (project name and BRANCH)')
    sys.exit()
  main(sys.argv)