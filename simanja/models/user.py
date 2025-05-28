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

def create_user(username, password, email):
    password_hash = generate_password_hash(password)
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Cek apakah username atau email sudah terdaftar
        cur.execute(
            "SELECT 1 FROM user_login WHERE user_name = %s OR email = %s",
            (username, email)
        )
        if cur.fetchone():
            print("Username atau email sudah terdaftar.")
            return False

        # Insert jika belum ada
        cur.execute(
            "INSERT INTO user_login (user_name, password_hash, email) VALUES (%s, %s, %s)",
            (username, password_hash, email)
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
        cur.execute("SELECT * FROM user_login WHERE user_name = %s", (username,))
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

