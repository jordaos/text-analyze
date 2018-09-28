import os
import sqlite3

def create_db(conn):
  conn.execute('DROP TABLE IF EXISTS sentiment;')
  conn.execute('''
      CREATE TABLE IF NOT EXISTS `sentiment` (
        `sha` TEXT, 
        `Positive` INTEGER, 
        `Negative` INTEGER, 
        `Text` TEXT, 
        `Explanation` TEXT )
    ''')
  conn.execute('DROP TABLE IF EXISTS commits;')
  conn.execute('''
    CREATE TABLE IF NOT EXISTS `commits` (
      `sha` TEXT, 
      `message` TEXT, 
      `date` TEXT,
      `insertions` INTEGER NULL,
      `deletions` INTEGER NULL)
    ''')
  conn.execute('DROP TABLE IF EXISTS refactorings;')
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
        change_package INTEGER,
        other INTEGER
      )
    ''')
  conn.execute('DROP TABLE IF EXISTS findings;')
  conn.execute('''
    CREATE TABLE IF NOT EXISTS `findings` (
      `sha` TEXT, 
      `new` INTEGER, 
      `unresolved` INTEGER,
      `resolved` INTEGER)
    ''')

def extract_data(conn, conn1):
  cursor = conn.cursor()
  cursor1 = conn1.cursor()
  cursor1.execute("SELECT * FROM commits;")
  commits = cursor1.fetchall()
  for linha in commits:
    sqlInsertCommit = 'INSERT INTO commits VALUES(?, ?, ?, ?, ?)'
    cursor.execute(sqlInsertCommit, linha)

  cursor1.execute("SELECT * FROM sentiment;")
  sentiments = cursor1.fetchall()
  for linha in sentiments:
    sqlInsertCommit = 'INSERT INTO sentiment (sha, Positive, Negative, Text, Explanation) VALUES (?, ?, ?, ?, ?)'
    cursor.execute(sqlInsertCommit, linha)

  cursor1.execute("SELECT * FROM refactorings;")
  refactorings = cursor1.fetchall()
  for linha in refactorings:
    sqlInsertRefactorings = 'INSERT INTO refactorings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cursor.execute(sqlInsertRefactorings, linha)

  cursor1.execute("SELECT * FROM findings;")
  findings = cursor1.fetchall()
  for linha in findings:
    sqlInsert = 'INSERT INTO findings VALUES(?,?,?,?)'
    cursor.execute(sqlInsert, linha)

  cursor.close()
  cursor1.close()


def insert_data(conn):
  data = './data'
  projects = [project for project in os.listdir(data) if os.path.isdir(os.path.join(data, project))]
  for project in projects:
    PATH = 'data/%s' % project
    conn1 = sqlite3.connect('%s/DB/%s.sqlite' % (PATH, project))
    conn1.text_factory = str
    extract_data(conn, conn1)


conn = sqlite3.connect('data/all.sqlite')
conn.text_factory = str

create_db(conn)
insert_data(conn)

conn.commit()
conn.close()

