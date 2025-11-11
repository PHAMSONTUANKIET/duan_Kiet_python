from common.updatedanhmuc import update_danh_muc

while True:
    madm = input("Nhập mã danh mục cần cập nhật: ")
    if not madm.isdigit():
        print("⚠️ Mã danh mục phải là số!")
        continue

    tendm = input("Nhập tên danh mục mới: ")

    ok = update_danh_muc(int(madm), tendm)

    if ok:
        print(f"✅ Cập nhật danh mục {madm} thành '{tendm}' thành công!")
    else:
        print(f"⚠️ Không tìm thấy danh mục có mã {madm}")

    con = input("Tiếp tục cập nhật? (y/n): ").lower()
    if con != "y":
        break
