from ketnoidb.ketnoi_mysql import connect_db
from mysql.connector import Error


def get_all_danh_muc():
    """
    Lấy toàn bộ danh mục từ bảng danhmuc.
    Trả về list các tuple (madm, tendm)
    """
    sql = "SELECT madm, tendm FROM danhmuc ORDER BY madm"

    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()  # [(1,'xxx'), (2,'yyy'), ...]

        cur.close()
        return rows

    except Error as e:
        raise RuntimeError(f"❌ Lỗi SELECT danh mục: {e}")

    finally:
        if conn:
            conn.close()
