import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error, IntegrityError

# dùng hàm connect_db() bạn đã có
from ketnoidb.ketnoi_mysql import connect_db


class DanhMucGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý Danh mục ")
        self.geometry("720x480")
        self.minsize(700, 420)

        # ====== FORM ======
        frm_form = ttk.LabelFrame(self, text="Thông tin danh mục", padding=10)
        frm_form.pack(fill="x", padx=10, pady=10)

        ttk.Label(frm_form, text="Mã danh mục (madm):").grid(row=0, column=0, sticky="w")
        self.var_madm = tk.StringVar()
        ttk.Entry(frm_form, textvariable=self.var_madm, state="readonly", width=12)\
            .grid(row=0, column=1, sticky="w", padx=(0, 15))

        ttk.Label(frm_form, text="Tên danh mục (tendm):").grid(row=0, column=2, sticky="w")
        self.var_tendm = tk.StringVar()
        ttk.Entry(frm_form, textvariable=self.var_tendm, width=35)\
            .grid(row=0, column=3, sticky="w")

        # ====== NÚT ======
        frm_btn = ttk.Frame(self)
        frm_btn.pack(fill="x", padx=10)

        ttk.Button(frm_btn, text="➕ Thêm",  command=self.add_dm).pack(side="left", padx=5, pady=5)
        ttk.Button(frm_btn, text="✏️ Sửa",   command=self.update_dm).pack(side="left", padx=5, pady=5)
        ttk.Button(frm_btn, text="🗑️ Xóa",   command=self.delete_dm).pack(side="left", padx=5, pady=5)
        ttk.Button(frm_btn, text="🧹 Xóa form", command=self.clear_form).pack(side="left", padx=5, pady=5)
        ttk.Button(frm_btn, text="🔄 Tải lại",  command=self.load_data).pack(side="left", padx=5, pady=5)

        # ====== BẢNG ======
        frm_table = ttk.Frame(self)
        frm_table.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frm_table, columns=("madm", "tendm"), show="headings", height=12)
        self.tree.heading("madm", text="Mã DM")
        self.tree.heading("tendm", text="Tên danh mục")
        self.tree.column("madm", width=80, anchor="center")
        self.tree.column("tendm", width=420, anchor="w")

        vsb = ttk.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frm_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frm_table.rowconfigure(0, weight=1)
        frm_table.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

        # nạp dữ liệu
        self.load_data()

    # ====== NGHIỆP VỤ ======
    def load_data(self):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT madm, tendm FROM danhmuc ORDER BY madm")
            rows = cur.fetchall()
            cur.close(); conn.close()
        except Error as e:
            messagebox.showerror("Lỗi DB", f"Không tải được danh sách: {e}")
            return

        for i in self.tree.get_children():
            self.tree.delete(i)
        for madm, tendm in rows:
            self.tree.insert("", "end", values=(madm, tendm))

    def clear_form(self):
        self.var_madm.set("")
        self.var_tendm.set("")
        self.tree.selection_remove(*self.tree.selection())

    def on_select_row(self, _ev=None):
        sel = self.tree.selection()
        if not sel: return
        madm, tendm = self.tree.item(sel[0], "values")
        self.var_madm.set(str(madm))
        self.var_tendm.set(tendm)

    def add_dm(self):
        tendm = self.var_tendm.get().strip()
        if not tendm:
            messagebox.showwarning("Thiếu thông tin", "Nhập TÊN danh mục (tendm).")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO danhmuc (tendm) VALUES (%s)", (tendm,))
            conn.commit()
            new_id = cur.lastrowid
            cur.close(); conn.close()
            messagebox.showinfo("Thành công", f"Đã thêm danh mục (madm={new_id}).")
            self.clear_form(); self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi DB", f"Không thêm được: {e}")

    def update_dm(self):
        madm = self.var_madm.get().strip()
        tendm = self.var_tendm.get().strip()
        if not madm:
            messagebox.showwarning("Chưa chọn", "Chọn 1 dòng để sửa.")
            return
        if not tendm:
            messagebox.showwarning("Thiếu thông tin", "Nhập TÊN danh mục (tendm).")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE danhmuc SET tendm=%s WHERE madm=%s", (tendm, madm))
            conn.commit()
            ok = cur.rowcount > 0
            cur.close(); conn.close()
            if ok:
                messagebox.showinfo("Thành công", f"Đã cập nhật danh mục (madm={madm}).")
                self.load_data()
            else:
                messagebox.showwarning("Không tìm thấy", f"Không có danh mục mã {madm}.")
        except Error as e:
            messagebox.showerror("Lỗi DB", f"Không sửa được: {e}")

    def delete_dm(self):
        madm = self.var_madm.get().strip()
        if not madm:
            messagebox.showwarning("Chưa chọn", "Chọn 1 dòng để xóa.")
            return
        if not messagebox.askyesno("Xác nhận", f"Xóa danh mục mã {madm}?"):
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM danhmuc WHERE madm=%s", (madm,))
            conn.commit()
            affected = cur.rowcount
            cur.close(); conn.close()
            if affected > 0:
                messagebox.showinfo("Thành công", f"Đã xóa danh mục (madm={madm}).")
                self.clear_form(); self.load_data()
            else:
                messagebox.showwarning("Không tìm thấy", f"Không có danh mục mã {madm}.")
        except IntegrityError as ie:
            # ví dụ 1451: FK sanpham.madm tham chiếu danhmuc.madm
            messagebox.showerror(
                "Không thể xóa",
                "Danh mục đang được sản phẩm sử dụng (khóa ngoại).\n"
                "• Xóa/đổi danh mục cho sản phẩm trước, hoặc\n"
                "• Sửa ràng buộc FK (CASCADE/SET NULL) nếu phù hợp nghiệp vụ."
            )
        except Error as e:
            messagebox.showerror("Lỗi DB", f"Lỗi khi xóa: {e}")


if __name__ == "__main__":
    DanhMucGUI().mainloop()
