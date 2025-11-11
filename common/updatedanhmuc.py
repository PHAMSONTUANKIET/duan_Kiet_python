from ketnoidb.ketnoi_mysql import connect_db
from mysql.connector import Error

def update_danh_muc(madm: int, tendm: str) -> bool:
    """
    Cập nhật tên danh mục theo mã madm.
    Trả về True nếu cập nhật thành công, False nếu mã không tồn tại.
    """
    sql = "UPDATE danhmuc SET tendm = %s WHERE madm = %s"

    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql, (tendm, madm))
        conn.commit()

        updated = cur.rowcount > 0
        cur.close()
        return updated

    except Error as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"❌ Lỗi UPDATE danh mục: {e}")

    finally:
        if conn:
            conn.close()
