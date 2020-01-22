
import requests
import sqlite3

def get_hh_vacancy():
  print("Setting variables.")
  baseurl = "https://api.hh.ru/"
  vacancies = baseurl + 'vacancies?'
  headers = {'User-Agent': 'My User Agent 1.0'}

  conn = sqlite3.connect('warehouse.db')
  cur = conn.cursor()

  print("Creating tables.")
  cur.executescript('''
  DROP TABLE IF EXISTS Vacancies;
  CREATE TABLE IF NOT EXISTS Vacancies (
    id INTEGER,
    salary_min INTEGER,
    salary_max INTEGER,
    name TEXT,
    area_id INTEGER,
    created TEXT
  )''')

  pagecounter = 0
  js = requests.get(vacancies + '&page=' + str(pagecounter) + '&per_page=100', headers=headers)
  pages = js.json()['pages']
  print("Opening URL: " + vacancies + '&page=' + str(pagecounter) + '&per_page=200')
  print("Total pages: " + str(pages))
  while pagecounter < pages:
    print("Retrieving vacancies. Page " + str(pagecounter + 1) + ". \n Opening URL: " + vacancies + '&page=' + str(
      pagecounter) + '&per_page=100')
    for item in js.json()['items']:
      if item['salary'] != None:
        cur.execute(
          '''INSERT OR IGNORE INTO Vacancies (id, salary_min, salary_max, name, area_id, created) VALUES ( ?, ?, ?, ?, ?, ? )''',
          (
          item['id'], item['salary']['from'], item['salary']['to'], item['name'], item['area']['id'], item['created_at']))
      else:
        cur.execute('''INSERT OR IGNORE INTO Vacancies (id, name, area_id, created) VALUES ( ?, ?, ?, ? )''',
                    (item['id'], item['name'], item['area']['id'], item['created_at']))
    pagecounter = pagecounter + 1
    js = requests.get(vacancies + '&page=' + str(pagecounter) + '&per_page=100', headers=headers)

  print("Writing changes to DB.")
  conn.commit()
  conn.close()
