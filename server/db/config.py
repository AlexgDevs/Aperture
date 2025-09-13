from os import getenv

from dotenv import load_dotenv

class DBSettings:
    def __init__(self, db_url: str, test_db_url: str, echo: bool = False):
        self.db_url = db_url
        self.test_db_url = test_db_url
        self.echo = echo

db_settings = DBSettings(
    db_url=getenv('DB_URL'), 
    test_db_url=getenv('TEST_DB_URL'), 
    echo=True
    )