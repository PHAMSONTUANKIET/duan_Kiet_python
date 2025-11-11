from common.getdanhmuc import get_all_danh_muc

ds = get_all_danh_muc()

print("📂 Danh sách danh mục của bạn :")

if not ds:
    print("⚠️ Không có danh mục nào!")
else:
    for row in ds:
        print(f"🆔 {row[0]}  |  📌 {row[1]}")
