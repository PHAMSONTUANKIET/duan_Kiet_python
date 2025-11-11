from ketnoidb.ketnoi_mysql import connect_db

conn = connect_db()

if conn:
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sanpham LIMIT 5;")
        data = cursor.fetchall()

        print("📦 Dữ liệu bảng sanpham:")
        for row in data:
            print(row)

    except Exception as err:
        print("❌ Lỗi khi truy vấn:", err)
    finally:
        conn.close()
        print("🔌 Đã đóng kết nối MySQL")
