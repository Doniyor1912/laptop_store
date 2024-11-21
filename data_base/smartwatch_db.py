import psycopg2
from config.config import Config
cfg = Config()
class Postgresql_smartwatch:
    def __init__(self):
        self.connect = psycopg2.connect(
            host=cfg.sm_host,
            user=cfg.sm_user,
            database=cfg.sm_db,
            password=cfg.sm_password
        )
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute(f"""
        DROP TABLE smartwatch;
        CREATE TABLE smartwatch(
            id SERIAL PRIMARY KEY,
            brand_name VARCHAR(240),
            brand_url TEXT,
            brand_photo VARCHAR(240),
            brand_price VARCHAR(240))
        """)
        self.connect.commit()

    def insert_data(self,*args):
        self.cursor.execute(f"""
        INSERT INTO smartwatch (brand_name, brand_url, brand_photo, brand_price)
        VALUES (%s,%s,%s,%s)""",args)
        self.connect.commit()

    def select_data(self):
        self.cursor.execute(f"""
        SELECT brand_name, brand_url, brand_photo, brand_price
        FROM smartwatch""")
        return self.cursor.fetchall()


