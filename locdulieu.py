import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Đọc dữ liệu từ file CSV
file_path = 'D:/python do an cuoi ki/cleaned_data.csv'
data = pd.read_csv(file_path)

# Chuẩn hóa tên cột
data.columns = data.columns.str.strip().str.lower()

# Hàm hiển thị dữ liệu
def display_data(tree, df):
    """Hiển thị dữ liệu lên giao diện Treeview."""
    tree.delete(*tree.get_children())
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Hàm xóa nội dung trong khu vực điều khiển
def clear_control_area(control_frame):
    for widget in control_frame.winfo_children():
        widget.destroy()

# Hàm hiển thị tất cả giá trị trong một cột
def display_column_values(column, listbox):
    """Hiển thị tất cả các giá trị duy nhất trong cột."""
    listbox.delete(0, tk.END)
    unique_values = data[column].dropna().unique()
    for value in unique_values:
        listbox.insert(tk.END, value)

# Hàm sắp xếp dữ liệu
def sort_data(tree, df, control_frame):
    clear_control_area(control_frame)

    tk.Label(control_frame, text="Chọn cột để sắp xếp:").pack(pady=5)
    column_var = ttk.Combobox(control_frame, values=list(df.columns))
    column_var.pack(pady=5)

    tk.Label(control_frame, text="Chọn thứ tự sắp xếp:").pack(pady=5)
    order_var = ttk.Combobox(control_frame, values=["Tăng dần", "Giảm dần"])
    order_var.pack(pady=5)

    def sort_action():
        selected_column = column_var.get()
        sort_order = order_var.get()
        if not selected_column or not sort_order:
            messagebox.showwarning("Thông báo", "Vui lòng chọn đầy đủ thông tin để sắp xếp.")
            return
        ascending = sort_order == "Tăng dần"
        sorted_df = df.sort_values(by=selected_column, ascending=ascending)
        display_data(tree, sorted_df)
        messagebox.showinfo("Thông báo", f"Dữ liệu đã được sắp xếp theo '{selected_column}' ({sort_order}).")

    tk.Button(control_frame, text="Sắp xếp", command=sort_action).pack(pady=10)

# Hàm lọc dữ liệu
def filter_data(tree, df, control_frame):
    clear_control_area(control_frame)

    tk.Label(control_frame, text="Chọn cột để lọc:").pack(pady=5)
    column_var = ttk.Combobox(control_frame, values=list(df.columns))
    column_var.pack(pady=5)

    tk.Label(control_frame, text="Nhập điều kiện lọc (vd: > 50):").pack(pady=5)
    condition_var = tk.Entry(control_frame)
    condition_var.pack(pady=5)

    # Listbox hiển thị các giá trị trong cột
    listbox = tk.Listbox(control_frame, height=10)
    listbox.pack(pady=5)

    def update_listbox(event):
        selected_column = column_var.get()
        if selected_column:
            display_column_values(selected_column, listbox)

    column_var.bind("<<ComboboxSelected>>", update_listbox)

    def filter_action():
        selected_column = column_var.get()
        filter_condition = condition_var.get()
        if not selected_column:
            messagebox.showwarning("Thông báo", "Vui lòng chọn cột để lọc.")
            return
        if not filter_condition:
            messagebox.showwarning("Thông báo", "Bạn chưa nhập điều kiện. Hiển thị toàn bộ dữ liệu.")
            display_data(tree, df)
            return
        try:
            filtered_df = df.query(f"{selected_column} {filter_condition}")
            display_data(tree, filtered_df)
            messagebox.showinfo("Thông báo", f"Dữ liệu đã được lọc với điều kiện '{selected_column} {filter_condition}'.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lọc dữ liệu: {str(e)}")

    tk.Button(control_frame, text="Lọc", command=filter_action).pack(pady=10)

# Hàm tìm kiếm dữ liệu
def search_data(tree, df, control_frame):
    clear_control_area(control_frame)

    tk.Label(control_frame, text="Chọn cột để tìm kiếm:").pack(pady=5)
    column_var = ttk.Combobox(control_frame, values=list(df.columns))
    column_var.pack(pady=5)

    # Listbox hiển thị các giá trị trong cột
    listbox = tk.Listbox(control_frame, height=10)
    listbox.pack(pady=5)

    def update_listbox(event):
        selected_column = column_var.get()
        if selected_column:
            display_column_values(selected_column, listbox)

    column_var.bind("<<ComboboxSelected>>", update_listbox)

    tk.Label(control_frame, text="Nhập từ khóa (hoặc chọn từ danh sách):").pack(pady=5)
    keyword_var = tk.Entry(control_frame)
    keyword_var.pack(pady=5)

    def search_action():
        selected_column = column_var.get()
        keyword = keyword_var.get()
        if not selected_column:
            messagebox.showwarning("Thông báo", "Vui lòng chọn cột để tìm kiếm.")
            return
        if not keyword:
            selected_item = listbox.get(tk.ACTIVE)  # Lấy giá trị được chọn trong Listbox
            if selected_item:
                keyword = selected_item
        result_df = df[df[selected_column].astype(str).str.contains(str(keyword), case=False, na=False)]
        display_data(tree, result_df)
        messagebox.showinfo("Thông báo", f"Tìm thấy {len(result_df)} kết quả trong cột '{selected_column}'.")

    tk.Button(control_frame, text="Tìm kiếm", command=search_action).pack(pady=10)

# Hàm xóa dữ liệu
def delete_data(tree, df, control_frame):
    clear_control_area(control_frame)

    tk.Label(control_frame, text="Chọn cột để xóa:").pack(pady=5)
    column_var = ttk.Combobox(control_frame, values=list(df.columns))
    column_var.pack(pady=5)

    # Listbox hiển thị các giá trị trong cột
    listbox = tk.Listbox(control_frame, height=10)
    listbox.pack(pady=5)

    def update_listbox(event):
        selected_column = column_var.get()
        if selected_column:
            display_column_values(selected_column, listbox)

    column_var.bind("<<ComboboxSelected>>", update_listbox)

    tk.Label(control_frame, text="Nhập giá trị cần xóa (hoặc chọn từ danh sách):").pack(pady=5)
    delete_value_var = tk.Entry(control_frame)
    delete_value_var.pack(pady=5)

    def delete_action():
        selected_column = column_var.get()
        value_to_delete = delete_value_var.get()
        if not selected_column:
            messagebox.showwarning("Thông báo", "Vui lòng chọn cột để xóa.")
            return
        if not value_to_delete:
            selected_item = listbox.get(tk.ACTIVE)  # Lấy giá trị được chọn trong Listbox
            if selected_item:
                value_to_delete = selected_item
        updated_df = df[df[selected_column] != value_to_delete]
        if len(updated_df) < len(df):
            global data
            data = updated_df  # Cập nhật dữ liệu toàn cục
            display_data(tree, data)
            messagebox.showinfo("Thông báo", f"Đã xóa các dòng chứa '{value_to_delete}' trong cột '{selected_column}'.")
        else:
            messagebox.showinfo("Thông báo", f"Không tìm thấy giá trị '{value_to_delete}' trong cột '{selected_column}'.")

    tk.Button(control_frame, text="Xóa", command=delete_action).pack(pady=10)

# Tạo giao diện chính
def main():
    root = tk.Tk()
    root.title("Quản lý Dữ liệu Âm nhạc")
    root.geometry("1200x800")

    # Frame hiển thị dữ liệu
    frame = ttk.LabelFrame(root, text="Dữ liệu Âm nhạc")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Treeview hiển thị dữ liệu
    tree = ttk.Treeview(frame, columns=list(data.columns), show="headings")
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)

    # Hiển thị dữ liệu ban đầu
    display_data(tree, data)

    # Frame các nút điều khiển
    control_frame = ttk.Frame(root)
    control_frame.pack(fill="x", padx=10, pady=10)

    # Frame cho chức năng chi tiết
    detail_frame = ttk.Frame(root)
    detail_frame.pack(fill="x", padx=10, pady=10)
    
    ttk.Button(control_frame, text="Sắp xếp dữ liệu", command=lambda: sort_data(tree, data, detail_frame)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Lọc dữ liệu", command=lambda: filter_data(tree, data, detail_frame)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Tìm kiếm dữ liệu", command=lambda: search_data(tree, data, detail_frame)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Xóa dữ liệu", command=lambda: delete_data(tree, data, detail_frame)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Thoát", command=root.quit).pack(side="right", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()