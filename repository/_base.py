import psycopg2


class PostgreDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='ec2-54-146-122-51.compute-1.amazonaws.com',
            database='db20jdmslac7gq',
            user='ywkuzugkfzxwrb',
            port='5432',
            password='a167300d9824476e5ec587ca485b6ebeac8720712e2d64a699a30643702307c8',
        )
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def queryParams(self, query, params):
        self.cur.execute(query, params)
        self.conn.commit()

    def fetchOne(self):
        return self.cur.fetchone()

    def fetchAll(self):
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
