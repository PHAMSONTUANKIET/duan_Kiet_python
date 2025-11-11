from ketnoidb.ketnoi_mysql import connect_db
from mysql.connector import Error

def delete_danh_muc(madm: int) -> bool:
    """
    Xoá danh mục theo madm.
    Trả về True nếu xoá thành công, False nếu không tìm thấy bản ghi.
    """
    sql = "DELETE FROM danhmuc WHERE madm = %s"

    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql, (madm,))
        conn.commit()

        deleted = cur.rowcount  # số dòng bị ảnh hưởng
        cur.close()

        return deleted > 0

    except Error as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"❌ Lỗi DELETE danh mục: {e}")

    finally:
        if conn:
            conn.close()
