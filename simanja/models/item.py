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
            "INSERT INTO assets.categories (category_code, category_name, category_alias) VALUES (%s, %s, %s)",
            (category_code, category_name, category_alias)
        )
        conn.commit()
        print("[DEBUG] INSERT success")
        return True
    except Exception as e:
        print(f"Error create_categories: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def update_category(category_id, category_name, category_alias, category_code):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE assets.categories
            SET category_name = %s, category_alias = %s, category_code = %s
            WHERE category_id = %s
        ''', (category_name, category_alias, category_code, category_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating category: {e}")
        return False

def delete_category_by_id(category_id):
    try:
        print(f"[DEBUG] model category_id: {category_id}")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM assets.categories WHERE category_id = %s', (category_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting category: {e}")
        return False

def get_all_categories():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM assets.categories ORDER BY category_id ASC")
        rows = cur.fetchall()
        # Digabung
        for r in rows:
            r['category_full_code'] = f"{r['category_alias']}-{r['category_code']}"
        return rows
    except Exception as e:
        print(f"Error get_all_categories: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_all_status():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM assets.item_status ORDER BY status_name")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Error get_all_status: {e}")
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
            INSERT INTO assets.items 
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
        cur.execute("SELECT * FROM assets.get_item_details()")
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

def update_item(item_id, item_name, category_id_item, received_date,
                status_id_item, location_id_name, take_out_date, end_date):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE assets.items
            SET item_name = %s,
                category_id_item = %s,
                received_date = %s,
                status_id_item = %s,
                location_id_name = %s,
                take_out_date = %s,
                end_date = %s
            WHERE item_id = %s
        ''', (
            item_name, category_id_item, received_date,
            status_id_item, location_id_name, take_out_date, end_date, item_id
        ))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating item: {e}")
        return False

def delete_item_by_id(item_id):
    try:
        print(f"[DEBUG] model item_id: {item_id}")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM assets.items WHERE item_id = %s', (item_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting item: {e}")
        return False