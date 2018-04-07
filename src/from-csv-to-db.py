import sqlite3
import sys
import csv
from subprocess import check_output
from classes.refactoringsEnum import RefactoringsEnum
from classes.commitRefactorings import CommitRefactorings
from classes.cd import cd

def create_db(PATH, PROJECT_NAME):
  conn = sqlite3.connect('%s/DB/%s.sqlite' % (PATH, PROJECT_NAME))
  conn.text_factory = str
  conn.execute('DROP TABLE IF EXISTS refactorings;')
  conn.execute('DROP TABLE IF EXISTS commits;')
  conn.execute('''
      CREATE TABLE IF NOT EXISTS refactorings (
        sha TEXT,
        total INTEGER,
        extract_method INTEGER,
        inline_method INTEGER,
        move_method_or_attribute INTEGER,
        pull_up_method_or_attribute INTEGER,
        push_down_method_or_attribute INTEGER,
        extract_superclass_or_interface INTEGER,
        move_class INTEGER,
        rename_class INTEGER,
        rename_method INTEGER,
        extract_and_move_method INTEGER,
        change_package INTEGER
      )
    ''')

  conn.execute('''
      CREATE TABLE IF NOT EXISTS commits (
        sha TEXT,
        message TEXT
      )
    ''')
  return conn

def insert(commit, conn, REPO_PATH):
  cursor = conn.cursor()
  rowsRefactorings = (commit.sha, commit.getTotal(), commit.getExtractedMethod(), commit.getInlineMethod(), commit.getMoveMethodOrAttribute(), commit.getPullUpMethodOrAttribute(), commit.getPushDownMethodOrAttribute(), commit.getExtractSuperclassOrInterface(), commit.getMoveClass(), commit.getRenameClass(), commit.getRenameMethod(), commit.getExtractAndMoveMethod(), commit.getChangePackage())
  sqlInsertRefactorings = 'INSERT INTO refactorings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
  
  commitMessage = ''
  with cd(REPO_PATH):
    commitMessage = check_output(['git', 'log', '--format=%B', '-n', '1', commit.sha])
  rowsCommit = (commit.sha, commitMessage)
  sqlInsertCommit = 'INSERT INTO commits VALUES(?, ?)'

  cursor.execute(sqlInsertRefactorings, rowsRefactorings)
  cursor.execute(sqlInsertCommit, rowsCommit)
  cursor.close()

def main(argv):
  PROJECT_NAME = argv[1]
  PATH = 'data/%s' % PROJECT_NAME
  ALL_REFACTORINGS_FILE = '%s/all_refactorings.csv' % PATH
  REPO_PATH = '%s/Repository/%s' % (PATH, PROJECT_NAME)
  conn = create_db(PATH, PROJECT_NAME)

  currentCommit = CommitRefactorings("")
  with open(ALL_REFACTORINGS_FILE) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
      refType = row[1].replace(' ', '')
      sha = row[0]
      if refType == 'RefactoringType':
        continue
      if currentCommit.sha == "":
        currentCommit = CommitRefactorings(sha)
      if(currentCommit.sha != sha):
        insert(currentCommit, conn, REPO_PATH)
        currentCommit = CommitRefactorings(sha)

      refactoringId = 0
      changePackageTypes = ['MoveSourceFolder', 'RenamePackage']
      if refType in changePackageTypes:
        refactoringId = RefactoringsEnum['ChangePackage'].value
      else:
        refactoringId = RefactoringsEnum[refType].value
      
      switchOptions = {
        1: currentCommit.addExtractedMethod,
        2: currentCommit.addInlineMethod,
        3: currentCommit.addMoveMethodOrAttribute,
        4: currentCommit.addPullUpMethodOrAttribute,
        5: currentCommit.addPushDownMethodOrAttribute,
        6: currentCommit.addExtractSuperclassOrInterface,
        7: currentCommit.addMoveClass,
        8: currentCommit.addRenameClass,
        9: currentCommit.addRenameMethod,
        10: currentCommit.addExtractAndMoveMethod,
        11: currentCommit.addChangePackage,
      }
      
      switchOptions[refactoringId]()

  # Para poder inserir o ultimo commit:
  insert(currentCommit, conn, REPO_PATH)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print 'Give parameter (project name)'
    sys.exit()
  main(sys.argv)