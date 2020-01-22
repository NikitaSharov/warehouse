import requests
import sqlite3

def sj_auth():
    url = 'https://api.superjob.ru/2.0/oauth2/password'
    params = {
        'login': 'nikita.sh37@yandex.ru',
        'password': '6217jx',
        'client_id': 	'1437',
        'client_secret': 'v3.r.131703652.d4c3ca1bed8ded9d2cd364db5735dece045fa01a.2d33f3811d062727f5c685a78df2617d100e8f13'
    }
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()['access_token']


def get_vacancies_sj(access_token, secret_key, cur):
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': secret_key,
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'count': 100,
    }
    vacancies = []
    for page in range(5):
        params['page'] = page
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        print(f'fetching {page}...')
        for item in response.json()['objects']:
            if item['payment_from']:
                cur.execute(
                '''INSERT OR IGNORE INTO Vacancies (id, salary_min, salary_max, name,created) VALUES ( ?, ?, ?, ?, ? )''',
                  (item['id'], item['payment_from'], item['payment_to'], item['profession'],
                   item['date_published']))
            else:
              # print item['id'], item['name'], item['area']['id'], item['created_at']
              cur.execute('''INSERT OR IGNORE INTO Vacancies (id, name,created) VALUES ( ?, ?, ? )''',
                          (item['id'], item['profession'], item['date_published']))

    return response.json()['total'], vacancies

def get_connection():
  conn = sqlite3.connect('warehouse.db')
  cur = conn.cursor()
  return cur,conn




def get_sj_vacancy():
  acess_token = sj_auth()
  cur,conn = get_connection()
  sum,vacancies = get_vacancies_sj(acess_token,'v3.r.131703652.d4c3ca1bed8ded9d2cd364db5735dece045fa01a.2d33f3811d062727f5c685a78df2617d100e8f13',cur)
  conn.commit()
  conn.close()
