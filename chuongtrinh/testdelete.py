from common.deletedanhmuc import delete_danh_muc

while True:
    madm = input("Nhập mã danh mục cần xoá: ")

    if madm.isdigit():
        ok = delete_danh_muc(int(madm))

        if ok:
            print(f"✅ Đã xoá danh mục có mã {madm}")
        else:
            print(f"⚠️ Không tìm thấy danh mục có mã {madm}")
    else:
        print("⚠️ Mã danh mục phải là số!")

    con = input("Tiếp tục xoá? (y/n): ").lower()
    if con != "y":
        break
