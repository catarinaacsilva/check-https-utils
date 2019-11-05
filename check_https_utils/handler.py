# coding: utf-8


__author__ = 'Catarina Silva'
__version__ = '0.1'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import csv
import logging
import psycopg2
import datetime


logger = logging.getLogger('DB')


class PostgreSQL():
    def __init__(self, host='localhost', port=5432, user='umqualquer', password='naomelembro', database='https'):
        self.connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        self.cursor = self.connection.cursor()

    def municipality_insert(self, name, url):
        try:
            self.cursor.execute('INSERT INTO municipality(name, url) VALUES (%s,%s)', (name, url))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)

    def municipality_select_name(self, name):
        try:
            self.cursor.execute('select url from municipality where name=%s', (name,))
            municipality_url = self.cursor.fetchone()[0]
            return municipality_url
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)
            return None
    
    def municipality_select_all(self):
        try:
            self.cursor.execute('select name from municipality')
            records = self.cursor.fetchall() 
            rv = []
            for row in records:
                rv.append(row[0])
            return rv
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)
            return []

    # Insert data into qualities table
    def qualities_insert(self, url, date, https, certificate, redirect, r301, hsts, no_http):
        try:
            self.cursor.execute('select id from municipality where url=%s', (url,))
            municipality_id = self.cursor.fetchone()[0]
            self.cursor.execute('INSERT INTO qualities(date, id, https, certificate, redirect, r301, hsts, no_http) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (date, municipality_id, https, certificate, redirect, r301, hsts, no_http))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)

    # Insert data into defects table
    def defects_insert(self, url, date, redirect, r301, similarity):
        try:
            self.cursor.execute('select id from municipality where url=%s', (url,))
            municipality_id = self.cursor.fetchone()[0]
            self.cursor.execute('INSERT INTO defects(date, id, redirect, r301, similarity) VALUES (%s, %s, %s, %s, %s)', (date, municipality_id, redirect, r301, similarity))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)
    
    # Insert data into data table (html and screenshot)
    def data_insert(self, url, date, html_raw, html_rendered, img):
        try:
            self.cursor.execute('select id from municipality where url=%s', (url,))
            municipality_id = self.cursor.fetchone()[0]
            self.cursor.execute('INSERT INTO data(date, id, html_raw, html_rendered, img) VALUES (%s, %s, %s, %s, %s)', (date, municipality_id, html_raw, html_rendered, img))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)
    
    def tests_select(self):
        try:
            self.cursor.execute('select distinct date from qualities')
            records = self.cursor.fetchall() 
            rv = []
            for row in records:
                rv.append(row[0])
            return rv
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)
    
    def test_select(self, name, date):
        try:
            self.cursor.execute('select id from municipality where name=%s', (name,))
            municipality_id = self.cursor.fetchone()[0]
            
            self.cursor.execute('select https,certificate,redirect,r301,hsts,no_http from qualities where id=%s and date=%s', (municipality_id, date))
            record = self.cursor.fetchone() 
            rv = {'date':date,
            'https':record[0],
            'certificate':record[1],
            'http_redirect': record[2],
            'http_r301':record[3],
            'hsts':record[4],
            'no_http':record[5]}
            
            self.cursor.execute('select redirect,r301,similarity from defects where id=%s and date=%s', (municipality_id, date))
            record = self.cursor.fetchone()
            rv['https_redirect']=record[0]
            rv['https_r301']=record[1]
            rv['similarity']=record[2]

            return rv
        except Exception as e:
            self.connection.rollback()
            logger.exception(e)
            return {}

    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def __del__(self):
        self.close()

#date =  datetime.datetime(2018, 11, 20)
#print(date)
#db = PostgreSQL(host='192.168.1.252')
#with open('defects.csv') as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=',')
#    for row in csv_reader:
#        url = row[0]
#        redirect = True if row[1] == 'TRUE' else False
#        r301 =  True if row[2] == 'TRUE' else False
#        similarity = float(row[3])
#        print('{} -> {} {} {}'.format(url, redirect, r301, similarity))
#        db.defects_insert(url, date, redirect, r301, similarity)
#db.close()