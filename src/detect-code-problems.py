import sqlite3
import sys
import csv
from subprocess import check_output, call
from classes.cd import cd

def compute_problems(sha, REPO_PATH):
  with cd(REPO_PATH):
    with cd(".git/"):
      call(["rm", "-f", "index.lock"])
    check_output(["git", "clean", "-d", "-fx"])
    check_output(["git", "checkout", sha])
    check_output(["../../../../tools/pmd-bin-6.2.0/bin/run.sh", "pmd", "-d", "./", "-f", "csv", "-R", "../../../../tools/pmd-bin-6.2.0/ruleset.xml", "-version", "1.7", "-language", "java", "-r", "../../pmd/%s-pmd.csv" % sha])

def main(argv):
  PROJECT_NAME = argv[1]
  PATH = 'data/%s' % PROJECT_NAME
  LOG_FILE_PATH = '%s/log.txt' % PATH
  REPO_PATH = '%s/Repository/%s' % (PATH, PROJECT_NAME)

  commits_sha = [line.split()[-1] for line in open(LOG_FILE_PATH) if "refactorings found in commit" in line]
  for sha in commits_sha:
    compute_problems(sha, REPO_PATH)
  

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print 'Give parameter (project name)'
    sys.exit()
  main(sys.argv)