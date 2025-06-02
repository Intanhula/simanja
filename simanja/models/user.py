import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from flask import session

def get_connection():
    return psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

def create_user(username, password, email):
    password_hash = generate_password_hash(password)
    WIB = timezone(timedelta(hours=7))
    now = datetime.now(WIB)

    created_by = session.get('username', 'system')  # fallback ke 'system' kalau belum login

    conn = get_connection()
    cur = conn.cursor()
    try:
        # Cek apakah username atau email sudah terdaftar
        cur.execute(
            "SELECT 1 FROM users WHERE username = %s OR email = %s",
            (username, email)
        )
        if cur.fetchone():
            print("Username atau email sudah terdaftar.")
            return False

        cur.execute(
            """
            INSERT INTO users 
            (username, password_hash, email, created_by, updated_by, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (username, password_hash, email, created_by, created_by, now, now)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error create_user: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def verify_login(username, password):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error verify_login: {e}")
        return False
    finally:
        cur.close()
        conn.close()

