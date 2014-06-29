import json
import mock
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask.ext.testing import TestCase
from helpscout_django import create_app as createapp


class APITest(TestCase):
    def setUp(self):
        # Create a test database, populate with dummy values
        c = self.app.config
        conn = psycopg2.connect(database='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute('CREATE DATABASE ' + c['DB_NAME'])
        conn.commit()
        conn.close()
        self.conn = psycopg2.connect(database=c['DB_NAME'], host=c['DB_HOST'], port=c['DB_PORT'])
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE auth_user (id SERIAL PRIMARY KEY, username TEXT, email VARCHAR(25))')
        cur.execute("INSERT INTO auth_user (username, email) VALUES ('u1', 'u1@abc.com')")
        self.conn.commit()

    def tearDown(self):
        # Drop test database
        self.conn.close()
        c = self.app.config
        conn = psycopg2.connect(database='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute('DROP DATABASE ' + c['DB_NAME'])
        conn.commit()
        conn.close()

    def test_something(self):
        with mock.patch('helpscout_django.decorators.is_helpscout_request') as MockClass:
            instance = MockClass.return_value
            instance.method.return_value = True

            # Invalid request without request body
            response = self.client.post("/get-user/")
            self.assertEquals(400, response.status_code)

            # Request for a user not in the database
            data = {'customer': {'email': 'u2@abc.com'}}
            response = self.client.post("/get-user/", headers=[('Content-Type', 'application/json')], data=json.dumps(data))
            self.assertEquals(404, response.status_code)

            # Valid user, verify HTML content
            data['customer']['email'] = 'u1@abc.com'
            response = self.client.post("/get-user/", headers=[('Content-Type', 'application/json')], data=json.dumps(data))
            reply = response.json
            self.assertTrue('html' in reply)
            self.assertEquals('<h3>u1</h3>', reply['html'].strip())

    def create_app(self):
        app = createapp(config_name='config_test')
        app.config['TESTING'] = True
        return app
