import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # đổi theo mật khẩu MySQL của bạn
            database="csdlnhathuocankhang"    # đổi thành tên DB bạn dùng
        )

        if conn.is_connected():
            print("✅ Kết nối MySQL thành công!")
            return conn

    except mysql.connector.Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")

