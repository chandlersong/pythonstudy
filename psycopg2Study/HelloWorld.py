import unittest
import urllib.parse as urlparse
import uuid
from datetime import datetime
from unittest import TestCase

import psycopg2
from psycopg2._json import Json


class TestHowToCreateConnection(TestCase):
    def test_create_simple_connection(self):
        try:
            conn = psycopg2.connect(
                "dbname='hodortest' user='postgres' host='192.168.0.119' port='5432' password='postgres'")
            print("create simple connection ok")
        except Exception as e:
            print(e)
            print("I am unable to connect to the database")

    def test_create_simple_connection_with_link(self):
        try:
            conn = psycopg2.connect(
                "postgresql://postgres:postgres@192.168.0.119:5432/hodortest")
            print("create simple connection with link ok")
        except Exception as e:
            print(e)
            print("I am unable to connect to the database")

    def test_create_simple_connection_with_url_parse(self):
        try:
            result = urlparse.urlparse("postgresql://postgres:postgres@192.168.0.119:5432/hodortest")
            username = result.username
            password = result.password
            database = result.path[1:]
            hostname = result.hostname
            connection = psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=hostname
            )
            print((database, hostname, username, password))
            print("test_create_simple_connection_with_url_parse ok")
        except Exception as e:
            print(e)
            print("I am unable to connect to the database")


class TestRunStatment(TestCase):
    def setUp(self):
        try:
            self.conn = psycopg2.connect(
                "postgresql://postgres:postgres@192.168.0.119:5432/hodortest")
            str_pattern = 'CREATE TABLE if not exists psycopg2_study( \
                                id uuid NOT NULL,\
                                stock_id character varying COLLATE pg_catalog."default" NOT NULL,\
                                stock_date timestamp without time zone NOT NULL,\
                                data jsonb NOT NULL,\
                                CONSTRAINT psycopg2_study_pkey PRIMARY KEY (id), \
                                CONSTRAINT psycopg2_study_minsuix_1 UNIQUE (stock_id, stock_date)\
                            )'
            with self.conn:
                with self.conn.cursor() as curs:
                    curs.execute(str_pattern)
                    self.conn.commit()
        except Exception as e:
            print(e)
            print("I am unable to connect to the database")

    def test_insert(self):
       insert_stmt = "insert into psycopg2_study (id,stock_id,stock_date,data) values (%s,%s,%s,%s)"
       with self.conn:
            with self.conn.cursor() as curs:
                json_data = Json({'a': 100})
                curs.execute(insert_stmt,(str(uuid.uuid1()),"abc",datetime(2005, 11, 18),json_data))
                self.conn.commit()

if __name__ == '__main__':
    unittest.main()
