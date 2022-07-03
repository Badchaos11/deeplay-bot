import os
from dotenv import load_dotenv

import pymysql.cursors


def create_connection() -> pymysql.Connection:
    load_dotenv()
    connection = pymysql.connect(host=str(os.getenv("HOST")),
                                 port=int(os.getenv("PORT")),
                                 user=str(os.getenv("USER")),
                                 password=str(os.getenv("PASSWORD")),
                                 database=str(os.getenv("DATABASE")),
                                 cursorclass=pymysql.cursors.DictCursor
                                 )
    return connection
