from ketnoidb.ketnoi_mysql import connect_db
from mysql.connector import Error

def insert_danh_muc(tendm: str) -> int:
    """
    Thêm danh mục vào bảng danhmuc.
    Trả về id vừa tạo.
    """
    sql = """
        INSERT INTO danhmuc (tendm)
        VALUES (%s)
    """

    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql, (tendm,))
        conn.commit()

        new_id = cur.lastrowid
        cur.close()
        return new_id

    except Error as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Lỗi INSERT danh muc: {e}")

    finally:
        if conn:
            conn.close()
