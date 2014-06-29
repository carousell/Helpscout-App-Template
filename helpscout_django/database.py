import psycopg2
from mosql.db import Database


class DjangoDatabase(Database):
    def __init__(self):
        pass

    def init_app(self, app):
        host = app.config['DB_HOST']
        name = app.config['DB_NAME']
        port = app.config['DB_PORT']
        user = app.config['DB_USER']
        password = app.config['DB_PASSWORD']
        super(DjangoDatabase, self).__init__(psycopg2, host=host, database=name,
                                             port=port, user=user, password=password)
