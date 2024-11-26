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
    # Làm mới Treeview để hiển thị dữ liệu mới
    for item in tree.get_children():
        tree.delete(item)
    for index, row in df.iterrows():
        tree.insert("", "end", values=row.tolist())

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

# Hàm thêm dữ liệu mới
# Hàm thêm dữ liệu mới
def add_new_data(df, tree, control_frame,root):
    clear_control_area(control_frame)

    tk.Label(control_frame, text="Nhập thông tin mới cho các cột:").pack(pady=5)

    # Dictionary để lưu các ô nhập liệu
    entry_fields = {}

    # Frame để chứa các ô nhập liệu
    input_frame = tk.Frame(control_frame)
    input_frame.pack(pady=10)

    # Chia các cột thành nhiều nhóm nhỏ (ví dụ: 2 cột trên mỗi dòng)
    num_columns_per_row = 4  # Số cột mỗi dòng sẽ chứa
    columns = list(df.columns)

    for i in range(0, len(columns), num_columns_per_row):
        row_frame = tk.Frame(input_frame)
        row_frame.pack(pady=5)
        
        # Tạo ô nhập liệu cho từng nhóm cột
        for column in columns[i:i + num_columns_per_row]:
            tk.Label(row_frame, text=f"{column}:").pack(side="left", padx=5)
            entry = tk.Entry(row_frame)
            entry.pack(side="left", padx=5)
            entry_fields[column] = entry  # Lưu ô nhập liệu vào dictionary

    def add_action():
        new_data = {}
        # Lấy giá trị từ các ô nhập liệu
        for column, entry in entry_fields.items():
            value = entry.get().strip()
            if value:  # Chỉ thêm dữ liệu nếu không trống
                new_data[column] = value

        # Nếu không có dữ liệu mới, cảnh báo người dùng
        if not new_data:
            messagebox.showwarning("Thông báo", "Vui lòng nhập ít nhất một giá trị.")
            return

        # Chuyển dữ liệu mới thành một dòng trong DataFrame
        new_row = pd.Series(new_data)

        # Thêm dòng mới vào DataFrame
        df.loc[len(df)] = new_row

        # Cập nhật Treeview để hiển thị dữ liệu mới
        display_data(tree, df)

        messagebox.showinfo("Thông báo", "Dữ liệu đã được thêm thành công.")
    
    # Hàm thoát chương trình
    def exit_program(root):
        root.quit()  # Thoát khỏi chương trình

    # Tạo nút "Thoát"
    exit_button = tk.Button(control_frame, text="Thoát", command=lambda: exit_program(root))
    exit_button.pack(side="right", padx=5, pady=10)

    # Tạo nút để thêm dữ liệu
    tk.Button(control_frame, text="Thêm dữ liệu", command=add_action).pack(pady=10)



def update_data(df, control_frame, tree):
    clear_control_area(control_frame)

    # Kiểm tra xem có dòng nào được chọn không
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng để cập nhật.")
        return

    # Lấy dữ liệu dòng được chọn
    selected_row = tree.item(selected_item[0])["values"]
    row_index = tree.index(selected_item[0])  # Chỉ số dòng trong DataFrame

    # Hiển thị thông tin dòng cần cập nhật
    tk.Label(control_frame, text="Cập nhật thông tin dòng đã chọn:").pack(pady=5)

    # Frame chứa các ô nhập liệu
    input_frame = tk.Frame(control_frame)
    input_frame.pack(pady=10, fill="x")

    entry_fields = []  # Danh sách các ô nhập liệu

    # Số cột trên mỗi hàng (3-4 dòng tùy thuộc số lượng cột)
    num_columns_per_row = 6  # 4 cột trên mỗi dòng
    columns = list(df.columns)

    # Chia cột thành nhiều dòng
    for i in range(0, len(columns), num_columns_per_row):
        for j, column in enumerate(columns[i:i + num_columns_per_row]):
            # Nhãn cột
            label = tk.Label(input_frame, text=f"{column}:", anchor="w", width=15)
            label.grid(row=i // num_columns_per_row * 2, column=j, padx=5, pady=5)  # Dòng chứa nhãn

            # Ô nhập liệu
            entry = tk.Entry(input_frame, width=20)
            entry.insert(0, selected_row[i + j])  # Chèn giá trị hiện tại
            entry.grid(row=i // num_columns_per_row * 2 + 1, column=j, padx=5, pady=5)  # Dòng chứa ô nhập liệu
            entry_fields.append(entry)

    # Hàm xử lý khi nhấn "Lưu"
    def update_action():
        # Lấy dữ liệu mới từ các ô nhập liệu
        updated_data = [entry.get().strip() for entry in entry_fields]

        # Kiểm tra nếu có ô nhập liệu trống
        if any(data == "" for data in updated_data):
            messagebox.showwarning("Thông báo", "Vui lòng điền đầy đủ thông tin.")
            return

        # Cập nhật DataFrame với dữ liệu mới
        for i, column in enumerate(df.columns):
            df.at[row_index, column] = updated_data[i]

        # Hiển thị lại Treeview
        display_data(tree, df)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được cập nhật thành công.")

        # Xóa nội dung khung điều khiển
        clear_control_area(control_frame)

    # Hàm xử lý khi nhấn "Thoát"
    def exit_action():
        clear_control_area(control_frame)  # Xóa nội dung khung điều khiển

    # Nút "Lưu" để xác nhận cập nhật
    tk.Button(control_frame, text="Lưu", command=update_action).pack(side="left", padx=10, pady=10)

    # Nút "Thoát" để hủy cập nhật
    tk.Button(control_frame, text="Thoát", command=exit_action).pack(side="left", padx=10, pady=10)





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

    tk.Label(control_frame, text="Nhập từ khóa:").pack(pady=5)
    keyword_var = tk.Entry(control_frame)
    keyword_var.pack(pady=5)

    def search_action():
        selected_column = column_var.get()
        keyword = keyword_var.get().strip()
        if not selected_column or not keyword:
            messagebox.showwarning("Thông báo", "Vui lòng chọn cột và nhập từ khóa.")
            return

        # Áp dụng thuật toán tìm kiếm tuần tự
        filtered_rows = []
        for index, value in enumerate(df[selected_column]):
            value_str = str(value).lower()  # Chuyển giá trị thành chuỗi (không phân biệt hoa/thường)
            if keyword.lower() in value_str:
                filtered_rows.append(df.iloc[index])  # Lấy dòng tương ứng nếu tìm thấy

        # Tạo DataFrame mới từ kết quả lọc
        filtered_df = pd.DataFrame(filtered_rows)

        # Hiển thị kết quả
        display_data(tree, filtered_df)
        messagebox.showinfo("Thông báo", f"Đã tìm thấy {len(filtered_rows)} kết quả.")

    tk.Button(control_frame, text="Tìm kiếm", command=search_action).pack(pady=10)

def delete_data(df, tree, control_frame):
    clear_control_area(control_frame)

    tk.Label(control_frame, text="Xóa dữ liệu được chọn:").pack(pady=5)

    def delete_action():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một dòng để xóa.")
            return

        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa {len(selected_items)} dòng dữ liệu không?")
        if not confirm:
            return

        # Thuật toán tìm kiếm và xóa tuần tự
        for item in selected_items:
            # Lấy chỉ số dòng trong Treeview
            row_index = tree.index(item)
            df.drop(index=row_index, inplace=True)

        # Reset lại chỉ số index trong DataFrame
        df.reset_index(drop=True, inplace=True)

        # Hiển thị lại dữ liệu
        display_data(tree, df)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được xóa thành công.")

    tk.Button(control_frame, text="Xóa", command=delete_action).pack(side="left", padx=5, pady=10)

def main():
    # Tạo giao diện chính
    root = tk.Tk()
    root.title("Quản lý Dữ liệu")

    # Tạo frame chứa Treeview để hiển thị dữ liệu
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True)

    # Tạo Treeview để hiển thị dữ liệu
    tree = ttk.Treeview(tree_frame, columns=list(data.columns), show="headings")
    for column in data.columns:
        tree.heading(column, text=column)
        tree.column(column, width=100)
    tree.pack(fill="both", expand=True)

    # Hiển thị dữ liệu
    display_data(tree, data)

    # Tạo khu vực điều khiển các chức năng
    control_frame = tk.Frame(root)
    control_frame.pack(fill="both", expand=True)

    # Tạo các nút điều khiển chức năng
    ttk.Button(control_frame, text="Thêm mới dữ liệu", command=lambda: add_new_data(data, tree, control_frame, root)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Cập nhật dữ liệu", command=lambda: update_data(data, control_frame, tree)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Xóa dữ liệu", command=lambda: delete_data(data, tree, control_frame)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Sắp xếp dữ liệu", command=lambda: sort_data(tree, data, control_frame)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Lọc dữ liệu", command=lambda: filter_data(tree, data, control_frame)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Tìm kiếm dữ liệu", command=lambda: search_data(tree, data, control_frame)).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()
