import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
def get_connection():
    return psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

def create_category(category_name, category_alias, category_code):
    conn = get_connection()
    cur = conn.cursor()
    print(f"[DEBUG] create_category called with: {category_code}, {category_name}, {category_alias}")
    try:
        print("[DEBUG] Executing INSERT")
        cur.execute(
            "INSERT INTO assets_category.asset_category (category_id, category_name, category_alias) VALUES (%s, %s, %s)",
            (category_code, category_name, category_alias)
        )
        conn.commit()
        print("[DEBUG] INSERT success")
        return True
    except Exception as e:
        print(f"Error create_category: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def get_all_categories():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT category_id, category_name, category_alias FROM assets_category.asset_category ORDER BY category_id")
        rows = cur.fetchall()
        # Digabung
        for r in rows:
            r['category_full_code'] = f"{r['category_alias']}-{r['category_id']}"
        return rows
    except Exception as e:
        print(f"Error get_all_categories: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def create_item(item_name, category_id_item, received_date, status_id_item, takeout_date=None):
    conn = get_connection()
    cur = conn.cursor()
    print(f"[DEBUG] create_item called with: {item_name}, {category_id_item}, {received_date}, {status_id_item}, {takeout_date}")
    try:
        print("[DEBUG] Executing INSERT")
        cur.execute(
            """
            INSERT INTO item_assets.item_asset 
            (item_name, category_id_item, received_date, status_id_item, takeout_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (item_name, category_id_item, received_date, status_id_item, takeout_date)
        )
        conn.commit()
        print("[DEBUG] INSERT success")
        return True
    except Exception as e:
        print(f"Error create_item: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def get_all_items():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM item_assets.get_item_details()")
        rows = cur.fetchall()

        # Cek isi data di console (untuk debugging)
        #print("[DEBUG] Hasil get_item_details:", rows)

        return rows

    except Exception as e:
        print(f"[ERROR] get_all_items: {e}")
        return []

    finally:
        cur.close()
        conn.close()
