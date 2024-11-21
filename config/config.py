import os

from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.getBotEnv()
        self.get_click()
        self.db_laptop()
        self.db_smartwatch()
        self.db_tv()


    def getBotEnv(self):
        self.token = os.getenv("TOKEN", "defaultbottoken")

    def get_click(self):
        self.click_token = os.getenv("CLICK_TOKEN","")

    def db_laptop(self):
        self.lp_host = os.getenv("DB_HOST", "")
        self.lp_user = os.getenv("DB_USER", "")
        self.lp_db = os.getenv("DB_NAME", "")
        self.lp_password = os.getenv("DB_PASSWORD", "")

    def db_smartwatch(self):
        self.sm_host = os.getenv("HOST", "")
        self.sm_user = os.getenv("USER", "")
        self.sm_db = os.getenv("NAME", "")
        self.sm_password = os.getenv("PASSWORD", "")

    def db_tv(self):
        self.tv_host = os.getenv("DATABASE_HOST", "")
        self.tv_user = os.getenv("DATABASE_USER", "")
        self.tv_db = os.getenv("DATABASE_NAME", "")
        self.tv_password = os.getenv("DATABASE_PASSWORD", "")