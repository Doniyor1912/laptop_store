import psycopg2
from config.config import Config
cfg = Config()
class Postgresql_laptop:
    def __init__(self):
        self.connect = psycopg2.connect(
            host=cfg.lp_host,
            user=cfg.lp_user,
            database=cfg.lp_db,
            password=cfg.lp_password
        )
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute(f"""
        DROP TABLE laptop;
        CREATE TABLE laptop(
            id SERIAL PRIMARY KEY,
            brand_name VARCHAR(240),
            brand_url TEXT,
            brand_photo VARCHAR(240),
            brand_price VARCHAR(240))
        """)
        self.connect.commit()

    def insert_data(self,*args):
        self.cursor.execute(f"""
        INSERT INTO laptop (brand_name, brand_url, brand_photo, brand_price)
        VALUES (%s,%s,%s,%s)""",args)
        self.connect.commit()

    def select_data(self):
        self.cursor.execute(f"""
        SELECT brand_name, brand_url, brand_photo, brand_price
        FROM laptop""")
        return self.cursor.fetchall()


