import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection():
    return psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

def create_user(username, password):
    password_hash = generate_password_hash(password)
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO user_login (user_name, password_hash) VALUES (%s, %s)",
            (username, password_hash)
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

def verify_user(username, password):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM user_login WHERE user_name = %s", (username,))
        user = cur.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error verify_user: {e}")
        return False
    finally:
        cur.close()
        conn.close()

