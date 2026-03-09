import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


def get_connection():
    
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    return conn


def create_reservation(name, people, time):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO reservations (name, people, time)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, people, time))

    conn.commit()

    cursor.close()
    conn.close()

    return "Reservation confirmed."
create_reservation("priyansh",2,"tonight")