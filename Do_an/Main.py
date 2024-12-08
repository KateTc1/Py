import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import imageio 
import DataChart as chart
import seaborn as sns



# Đọc dữ liệu từ file CSV
file_path = r"cleaned_data.csv"
data = pd.read_csv(file_path)  # hoặc 'cp1252'


# Chuẩn hóa tên cột
data.columns = data.columns.str.strip()

# Lưu file
def save_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print(f"Dữ liệu đã được lưu vào {file_path}")
    except Exception as e:
        print(f"Không thể lưu dữ liệu: {e}")

chart_options = {
    "Biểu đồ thể hiện sự phân bố của các dữ liệu" : lambda:chart.Over_view(data),
    "Biểu đồ nhiệt thể hiện sự tương quan các chỉ số" : lambda:chart.heat_map(data),
    "Biểu đồ thể hiện sự tương quan giữa Acoustic và Energy": lambda:chart.scattter_acoustic_vs_energy(data),
    "Xu hướng của các đặc trưng âm thanh qua từng năm" : lambda:chart.Trend_of_sound_feature(data),
    "Top 10 nghệ sĩ có nhiều bài hit nhất": lambda:chart.Top_10_Artist(data),
    "Top 10 album có nhiều bài hit nhất" : lambda:chart.Top_10_album_most_song(data),
    "Top 10 track có phổ biến nhất: " : lambda:chart.TopTrack(data),
    "Lượng nghe trung bình của các bài hát qua từn năm" : lambda:chart.Mean_Popularity_Track_Over_Year(data),
    "So sánh độ phổ biến của các bài hát solo và collab" : lambda:chart.Comparison_solo_collab(data)
}



# Hàm xóa nội dung trong khu vực điều khiển
def clear_control_area(control_frame):
    for widget in control_frame.winfo_children():
        widget.destroy()

# Hàm tạo giao diện chọn hình ảnh từ combobox
def show_chart_list(control_frame):
    # Tạo cửa sổ pop-up mới
    pop_up = tk.Toplevel(control_frame)
    pop_up.title("Chọn biểu đồ để vẽ")
    pop_up.geometry("300x250")  # Kích thước cửa sổ pop-up

    # Tạo tiêu đề
    tk.Label(pop_up, text="Chọn biểu đồ để vẽ:").pack(pady=10)

    # Tạo combobox để chọn biểu đồ
    chart_combobox = ttk.Combobox(pop_up, values=list(chart_options.keys()))
    chart_combobox.pack(pady=10)

    # Hàm để vẽ biểu đồ đã chọn
    def draw_selected_chart():
        selected_chart = chart_combobox.get()
        if selected_chart:
            # Gọi hàm vẽ tương ứng
            chart_function = chart_options.get(selected_chart)
            if chart_function:
                chart_function()
        else:
            messagebox.showwarning("Thông báo", "Vui lòng chọn biểu đồ.")

    # Nút "Vẽ biểu đồ"
    ttk.Button(pop_up, text="Vẽ biểu đồ", command=draw_selected_chart).pack(pady=10)
    
    # Nút "Thoát" để đóng pop-up
    ttk.Button(pop_up, text="Thoát", command=pop_up.destroy).pack(pady=10)



# PHÂN TRANG
rows_per_page = 100  # Số dòng mỗi trang
current_page = 0  # Trang hiện tại

# HIỂN THỊ DỮ LIỆU
# Hiển thị trang

def display_page(tree, df, page):
    start_row = page * rows_per_page
    end_row = start_row + rows_per_page
    page_data = df.iloc[start_row:end_row]
    display_data(tree, page_data)


def display_data(tree, df):
    """Hiển thị dữ liệu lên giao diện Treeview."""
    tree.delete(*tree.get_children())
    for row in df.to_numpy():
        tree.insert("", "end", values=list(row))
def display_data(tree, df):
    """Hiển thị dữ liệu lên Treeview."""
    # Xóa dữ liệu hiện tại trong Treeview
    tree.delete(*tree.get_children())

    # Thêm dữ liệu mới vào Treeview
    for _, row in df.iterrows():
        tree.insert("", "end", values=row.tolist())

# DÒNG CẬP NHẬT TRẠNG THÁI
def update_status(message, color="green"):
    status_label.config(text=message, fg=color)

# HÀM ĐIỀU HƯỚNG 
def next_page(tree, df):
    global current_page
    global sorted_df  # Kiểm tra xem có DataFrame đã sắp xếp không
    data = sorted_df if 'sorted_df' in globals() else df

    if (current_page + 1) * rows_per_page < len(data):
        current_page += 1
        display_page(tree, data, current_page)
        update_status(f"Trang hiện tại: {current_page + 1}")
    else:
        messagebox.showinfo("Thông báo", "Đây là trang cuối cùng.")



def prev_page(tree, df):
    global current_page
    global sorted_df  # Kiểm tra xem có DataFrame đã sắp xếp không
    data = sorted_df if 'sorted_df' in globals() else df

    if current_page > 0:
        current_page -= 1
        display_page(tree, data, current_page)
        update_status(f"Trang hiện tại: {current_page + 1}")
    else:
        messagebox.showinfo("Thông báo", "Đây là trang đầu tiên.")


# Hàm TÌM KIẾM DỮ LIỆU
def search_data(tree, df, button_frame):
    # Tạo một pop-up nhỏ cho tìm kiếm
    search_window = tk.Toplevel()
    search_window.title("Tìm kiếm Dữ liệu")
    search_window.geometry("400x250")  # Kích thước cửa sổ pop-up

    # Giao diện trong pop-up
    tk.Label(search_window, text="Chọn cột để tìm kiếm:").pack(pady=5)
    column_var = ttk.Combobox(search_window, values=list(df.columns))
    column_var.pack(pady=5)

    tk.Label(search_window, text="Nhập từ khóa:").pack(pady=5)
    keyword_var = tk.Entry(search_window)
    keyword_var.pack(pady=5)

    # Hàm xử lý khi nhấn nút Tìm kiếm
    def search_action():
        selected_column = column_var.get()
        keyword = keyword_var.get().strip()

        if not selected_column or not keyword:
            messagebox.showwarning("Thông báo", "Vui lòng chọn cột và nhập từ khóa.")
            return

        # Áp dụng thuật toán tìm kiếm
        filtered_rows = []
        for index, value in enumerate(df[selected_column]):
            value_str = str(value).lower()  # Chuyển giá trị thành chuỗi (không phân biệt hoa/thường)
            if keyword.lower() in value_str:
                filtered_rows.append(df.iloc[index])  # Lấy dòng tương ứng nếu tìm thấy

        # Kiểm tra kết quả tìm kiếm
        if not filtered_rows:
            messagebox.showinfo("Thông báo", "Không tìm thấy kết quả nào.")
            return

        # Tạo DataFrame mới từ kết quả lọc
        filtered_df = pd.DataFrame(filtered_rows)

        # Hiển thị kết quả trên Treeview
        display_data(tree, filtered_df)
        messagebox.showinfo("Thông báo", f"Đã tìm thấy {len(filtered_rows)} kết quả.")
        
        # Đóng cửa sổ tìm kiếm
        search_window.destroy()

    # Nút Tìm kiếm
    tk.Button(search_window, text="Tìm kiếm", command=search_action).pack(pady=10)

    # Nút Hủy hoặc Đóng pop-up
    tk.Button(search_window, text="Đóng", command=search_window.destroy).pack(pady=5)

# Hàm SẮP XẾP DỮ LIỆU
# Cập nhật hàm sort_data để sắp xếp toàn bộ DataFrame và hiển thị lại các trang
# Sắp xếp toàn bộ DataFrame và cập nhật hiển thị
def sort_data(tree, df):
    def sort_action():
        selected_column = column_var.get()
        sort_order = order_var.get()
        if not selected_column or not sort_order:
            messagebox.showwarning("Thông báo", "Vui lòng chọn đầy đủ thông tin để sắp xếp.")
            return

        ascending = sort_order == "Tăng dần"
        
        # Cập nhật toàn bộ DataFrame với dữ liệu đã sắp xếp
        global current_page
        global sorted_df  # Lưu DataFrame đã sắp xếp vào một biến toàn cục để sử dụng cho phân trang
        sorted_df = df.sort_values(by=selected_column, ascending=ascending)

        # Reset lại trang hiện tại và hiển thị trang đầu tiên
        current_page = 0
        display_page(tree, sorted_df, current_page)
        
        update_status(f"Dữ liệu đã được sắp xếp theo '{selected_column}' ({sort_order}).")
        sort_window.destroy()

    # Tạo cửa sổ pop-up cho sắp xếp
    sort_window = tk.Toplevel()
    sort_window.title("Sắp xếp dữ liệu")
    sort_window.geometry("300x200")

    tk.Label(sort_window, text="Chọn cột để sắp xếp:").pack(pady=5)
    column_var = ttk.Combobox(sort_window, values=list(df.columns))
    column_var.pack(pady=5)

    tk.Label(sort_window, text="Chọn thứ tự sắp xếp:").pack(pady=5)
    order_var = ttk.Combobox(sort_window, values=["Tăng dần", "Giảm dần"])
    order_var.pack(pady=5)

    ttk.Button(sort_window, text="Xác nhận", command=sort_action).pack(pady=10)


# ============================ Hàm LỌC DỮ LIỆU ============================
def filter_data(tree, df, control_frame):
    # Tạo cửa sổ pop-up cho việc lọc dữ liệu
    filter_window = tk.Toplevel()
    filter_window.title("Lọc Dữ Liệu")
    filter_window.geometry("400x300")  # Kích thước cửa sổ nhỏ
    filter_window.grab_set()  # Khóa cửa sổ cha cho đến khi pop-up đóng

    # Tạo giao diện chọn cột và nhập điều kiện lọc cho các cột
    tk.Label(filter_window, text="Chọn cột để lọc 1:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    column_var1 = ttk.Combobox(filter_window, values=list(df.columns))
    column_var1.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(filter_window, text="Nhập điều kiện lọc 1 (vd: > 50 không dùng cho chữ và ngày tháng năm):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    condition_var1 = tk.Entry(filter_window)
    condition_var1.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Tạo các phần tử lọc cho các cột còn lại (nếu có)
    columns_vars = [column_var1]
    conditions_vars = [condition_var1]
    for i in range(2, 4):
        row_offset = (i-1) * 2 + 2  # Đảm bảo các phần tử lọc không bị đè lên nhau
        tk.Label(filter_window, text=f"Chọn cột để lọc {i} (nếu có):").grid(row=row_offset, column=0, padx=10, pady=5, sticky="w")
        column_var = ttk.Combobox(filter_window, values=list(df.columns))
        column_var.grid(row=row_offset, column=1, padx=10, pady=5, sticky="w")
        columns_vars.append(column_var)

        tk.Label(filter_window, text=f"Nhập điều kiện lọc {i} (nếu có):").grid(row=row_offset + 1, column=0, padx=10, pady=5, sticky="w")
        condition_var = tk.Entry(filter_window)
        condition_var.grid(row=row_offset + 1, column=1, padx=10, pady=5, sticky="w")
        conditions_vars.append(condition_var)

    # Hàm xử lý khi nhấn nút "Lọc"
    def filter_action():
        filter_conditions = []

        # Lấy giá trị cột và điều kiện lọc cho các cột
        for column_var, condition_var in zip(columns_vars, conditions_vars):
            column = column_var.get()
            condition = condition_var.get().strip()
            if column and condition:  # Nếu có cả cột và điều kiện
                filter_conditions.append((column, condition))

        # Kiểm tra đầu vào
        if not filter_conditions:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một cột và nhập điều kiện lọc.")
            return

        try:
            filtered_df = df

            # Lọc dữ liệu theo các điều kiện
            for column, condition in filter_conditions:
                # Xử lý điều kiện lọc tùy thuộc vào kiểu dữ liệu của cột
                column_dtype = filtered_df[column].dtype

                # Xử lý dữ liệu kiểu datetime
                if pd.api.types.is_datetime64_any_dtype(filtered_df[column]):
                    operator, date_value = condition.split(" ", 1)
                    date_value = pd.to_datetime(date_value, errors="coerce")
                    if pd.isna(date_value):
                        raise ValueError(f"Định dạng ngày tháng không hợp lệ trong cột {column}. Sử dụng định dạng YYYY-MM-DD.")
                    filtered_df = filtered_df.query(f"`{column}` {operator} @date_value")

                # Xử lý dữ liệu kiểu số
                elif pd.api.types.is_numeric_dtype(filtered_df[column]):
                    filtered_df = filtered_df.query(f"`{column}` {condition}")
                # Xử lý dữ liệu kiểu chuỗi (string)
                elif pd.api.types.is_string_dtype(filtered_df[column]):
                    if "==" in condition or "!=" in condition:
                        filtered_df = filtered_df.query(f"`{column}` {condition}")
                    else:
                        # Sử dụng phương thức .str.contains() để lọc chuỗi
                        filtered_df = filtered_df[filtered_df[column].str.contains(condition, case=False, na=False)]

                # Xử lý các loại dữ liệu không được hỗ trợ
                else:
                    raise ValueError(f"Loại dữ liệu không được hỗ trợ cho cột '{column}'.")

            # Hiển thị dữ liệu sau khi lọc
            display_data(tree, filtered_df)
            messagebox.showinfo("Thông báo", "Dữ liệu đã được lọc thành công.")
            filter_window.destroy()  # Đóng cửa sổ lọc sau khi hoàn tất

        except ValueError as ve:
            messagebox.showerror("Lỗi", f"Lỗi khi lọc dữ liệu: {ve}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi không xác định: {str(e)}")

    # Nút "Lọc" và "Thoát"
    button_frame = ttk.Frame(filter_window)
    button_frame.grid(row=10, column=0, columnspan=2, pady=18)

    # Nút "Lọc"
    tk.Button(button_frame, text="Lọc", command=filter_action, width=20).grid(row=3, column=0, padx=8, pady=12)

    # Nút "Thoát"
    tk.Button(button_frame, text="Thoát", command=filter_window.destroy, width=20).grid(row=3, column=1, padx=8, pady=12)


# Hàm hiển thị tất cả giá trị trong một cột
def display_column_values(column, listbox):
    """Hiển thị tất cả các giá trị duy nhất trong cột."""
    listbox.delete(0, tk.END)
    unique_values = data[column].dropna().unique()
    for value in unique_values:
        listbox.insert(tk.END, value)

# Hàm hiển thị dữ liệu trong Treeview
def display_data(tree, df):
    for item in tree.get_children():
        tree.delete(item)
    for _, row in df.iterrows():
        tree.insert("", "end", values=row.tolist())

import re
numeric_columns = [
    "Danceability", "Energy", "Key", "Loudness", "Mode", "Speechiness", 
    "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", 
    "Time Signature", "Popularity", "Disc Number", "Track Number", "Track Duration (ms)"
]
def update_data(df, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng để cập nhật.")
        return

    # Lấy thông tin dòng đã chọn từ Treeview
    selected_row = tree.item(selected_item[0])["values"]
    # Tìm dòng dựa trên cột đầu tiên, nếu không tìm được, kiểm tra các cột khác
    row_index = None
    for col_index in range(len(df.columns)):
        try:
            row_index = df.index[df.iloc[:, col_index] == selected_row[col_index]].tolist()[0]
            break  # Thoát khỏi vòng lặp nếu tìm được
        except (IndexError, KeyError):
            continue  # Nếu không tìm thấy trong cột này, kiểm tra cột tiếp theo

    if row_index is None:
        messagebox.showerror("Lỗi", "Không tìm thấy dòng phù hợp trong bảng dữ liệu.")
        return

    update_window = tk.Toplevel()
    update_window.title("Cập nhật dữ liệu")
    update_window.geometry("800x400")

    tk.Label(update_window, text="Cập nhật thông tin dòng đã chọn:").pack(pady=5)

    input_frame = tk.Frame(update_window)
    input_frame.pack(pady=10, fill="x")

    entry_fields = []
    columns = list(df.columns)

    # Tạo một cửa sổ nhập liệu với các cột
    row = 0
    col = 0
    for i, column in enumerate(columns):
        label = tk.Label(input_frame, text=f"{column}:", anchor="w", width=15)
        label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        # Tạo ô nhập liệu
        entry = tk.Entry(input_frame, width=30)

        # Kiểm tra giá trị của cột trong selected_row
        value = selected_row[i] if i < len(selected_row) else ""

        entry.insert(0, str(value))
        entry.grid(row=row, column=col + 1, padx=5, pady=5)
        entry_fields.append(entry)

        # Hàm kiểm tra xem dữ liệu nhập vào có phải là số hợp lệ không
        def validate_date_input(P):
            if P == "" or re.match(r"^\d{4}-\d{2}-\d{2}$", P):  # Kiểm tra định dạng yyyy-mm-dd
                return True
            return False

        # Hàm kiểm tra kiểu boolean cho cột Explicit
        def validate_boolean_input(P):
            if P == "" or P.lower() in ["true", "false"]:  # Chấp nhận "true", "false" (không phân biệt chữ hoa/thường)
                return True
            return False

        # Hàm kiểm tra kiểu số (số nguyên hoặc số thực)
        def validate_number_input(P):
            if P == "" or re.match(r'^-?\d+(\.\d+)?$', P):  # Chấp nhận số nguyên hoặc số thực
                return True
            return False



        # Kiểm tra kiểu dữ liệu của cột
        # Kiểm tra kiểu dữ liệu của cột
        # if column == "Explicit":  # Kiểm tra riêng cột Explicit
        #     validate_cmd = update_window.register(validate_boolean_input)  # Đăng ký hàm kiểm tra cho boolean
        #     entry = tk.Entry(input_frame, width=20, validate="key", validatecommand=(validate_cmd, "%P"))
        # else:
            # Kiểm tra cho các cột số (numeric)
        if pd.api.types.is_numeric_dtype(df[column]) and column != "Explicit":
                validate_cmd = update_window.register(validate_number_input)  # Đăng ký hàm kiểm tra cho số
                entry = tk.Entry(input_frame, width=20, validate="key", validatecommand=(validate_cmd, "%P"))
        else:
                entry = tk.Entry(input_frame, width=20)  # Các cột khác


        # Gán giá trị vào ô nhập liệu sau khi kiểm tra
        value = selected_row[i]

        # if isinstance(value, bool):  # Nếu giá trị là boolean (True/False)
        #     entry.insert(0, "True" if value else "False")  # Điền "True" hoặc "False"
        if isinstance(value, (int, float)):  # Nếu giá trị là số (int hoặc float)
            entry.insert(0, f"{value:.2f}" if isinstance(value, float) else str(value))
        else:  # Nếu giá trị là chuỗi (văn bản)
            entry.insert(0, str(value))  # Điền chuỗi vào ô nhập liệu

        col += 2  # Mỗi cột chiếm 2 cột trong grid (1 cho Label và 1 cho Entry)
        if col >= 8:  # Nếu đã đầy 4 cột (4 cặp cột label-entry)
            col = 0
            row += 1

    # Hàm xử lý khi nhấn "Lưu"
    # Hàm xử lý khi nhấn "Lưu"
    def confirm_update():
        updated_data = [entry.get().strip() for entry in entry_fields]

        # Kiểm tra xem có ô nào trống không
        if any(data == "" for data in updated_data):
            messagebox.showwarning("Thông báo", "Vui lòng điền đầy đủ thông tin.")
            return

        # Kiểm tra định dạng dữ liệu nhập vào
        is_valid, error_message = validate_input(updated_data, df)
        if not is_valid:
            messagebox.showwarning("Thông báo", error_message)
            return

        # Cập nhật dữ liệu vào DataFrame
        # Cập nhật dữ liệu vào DataFrame
        for i, column in enumerate(columns):
            if column == "Album Release Date":
                # Kiểm tra định dạng ngày tháng và cập nhật
                try:
                    pd.to_datetime(updated_data[i], format='%Y-%m-%d')
                    df.at[row_index, column] = updated_data[i]
                except ValueError:
                    messagebox.showwarning("Thông báo", f"Định dạng ngày tháng không hợp lệ cho cột {column}. Hãy nhập theo định dạng YYYY-MM-DD.")
                    return
            # elif column == "Explicit":
            #     # Kiểm tra giá trị cho cột Explicit (chỉ chấp nhận True hoặc False)
            #     value = updated_data[i].strip().lower()  # Chuyển giá trị nhập thành chữ thường để so sánh
            #     if value not in ["true", "false"]:  # Chỉ chấp nhận "true" hoặc "false"
            #         messagebox.showwarning("Thông báo", f"Giá trị không hợp lệ cho cột {column}. Chỉ chấp nhận 'True' hoặc 'False'.")
            #         return
            #     # Cập nhật giá trị vào DataFrame, chuyển 'true'/'false' thành True/False boolean
            #     df.at[row_index, column] = True if value == "true" else False
            else:
                if column in numeric_columns:
                    try:
                        df.at[row_index, column] = float(updated_data[i]) if '.' in updated_data[i] else int(updated_data[i])
                    except ValueError:
                        messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {updated_data[i]} cho cột {column}")
                        return
                else:
                    df.at[row_index, column] = updated_data[i]  # Cập nhật Treeview

        # Sau khi cập nhật dữ liệu, hiển thị lại dữ liệu trong Treeview
        display_data(tree, df)
        save_to_csv(df, file_path)


        # Thông báo thành công
        messagebox.showinfo("Thông báo", "Dữ liệu đã được cập nhật thành công.")
        update_window.destroy()


    # Nút "Lưu"
    button_frame = tk.Frame(update_window)  # Tạo một Frame riêng cho các nút
    button_frame.pack(side="bottom", fill="x", pady=10)

    confirm_button = ttk.Button(button_frame, text="Lưu", command=confirm_update)
    confirm_button.grid(row=0, column=0, padx=10)

    # Nút "Thoát"
    def exit_action():
        update_window.destroy()

    cancel_button = ttk.Button(button_frame, text="Thoát", command=exit_action)
    cancel_button.grid(row=0, column=1, padx=10)




def add_update_button(button_frame, df, tree):
    """
    The function `add_update_button` adds a button to a specified frame that updates a DataFrame and a
    treeview widget.
    
    :param button_frame: The `button_frame` parameter is likely a tkinter Frame widget where you want to
    place the update button. This button will be used to trigger an update action related to the data
    displayed in the `tree` widget, which is typically a ttk.Treeview widget. The `df` parameter is
    likely a
    :param df: The `df` parameter is typically used to represent a DataFrame in Python, which is a
    two-dimensional, size-mutable, potentially heterogeneous tabular data structure with labeled axes
    (rows and columns). It is commonly used in data analysis and manipulation with libraries such as
    Pandas
    :param tree: The `tree` parameter is likely referring to a Treeview widget in a GUI application.
    Treeview widgets are commonly used to display tabular data in a hierarchical structure, similar to a
    tree. In this context, the `tree` parameter is likely being used to represent the Treeview widget
    where data
    """
    ttk.Button(button_frame, text="Cập nhật dữ liệu", command=lambda: update_data(df, tree)).pack(side="left", padx=5)

def create_window(df):
    window = tk.Tk()
    window.title("Cập nhật dữ liệu")

    tree = ttk.Treeview(window, columns=list(df.columns), show="headings")
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=20)

    display_data(tree, df)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    add_update_button(button_frame, df, tree)

    window.mainloop()

# ======================== HÀM XOÁ DỮ LIỆU ===================
def delete_data(df, tree):
    # Lấy tất cả các dòng được chọn trong Treeview
    selected_items = tree.selection()

    if not selected_items:
        messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một dòng để xóa.")
        return

    # Xác nhận xóa
    if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa {len(selected_items)} dòng đã chọn?"):
        return

    # Danh sách lưu chỉ số của các dòng cần xóa
    selected_indices = []

    # Lấy dữ liệu dòng đã chọn từ Treeview và tìm chỉ số trong DataFrame
    for item in selected_items:
        selected_row = tree.item(item)["values"]  # Lấy dữ liệu của dòng từ Treeview

        # Tìm chỉ số dòng trong DataFrame dựa vào các cột
        row_index = None
        for col_index in range(len(df.columns)):
            try:
                row_index = df.index[df.iloc[:, col_index] == selected_row[col_index]].tolist()[0]
                break  # Thoát vòng lặp nếu tìm thấy
            except (IndexError, KeyError):
                continue  # Nếu không tìm thấy trong cột này, kiểm tra cột tiếp theo

        # Nếu tìm thấy dòng, thêm chỉ số vào danh sách
        if row_index is not None:
            selected_indices.append(row_index)

    # Nếu không tìm thấy bất kỳ dòng nào
    if not selected_indices:
        messagebox.showinfo("Thông báo", "Không tìm thấy dòng nào để xóa.")
        return

    # Xóa các dòng đã chọn trong DataFrame
    df.drop(index=selected_indices, inplace=True)

    # Cập nhật lại chỉ số chỉ mục của DataFrame
    df.reset_index(drop=True, inplace=True)

    # Cập nhật lại Treeview
    display_data(tree, df)

    # Lưu DataFrame vào CSV
    save_to_csv(df, "cleaned_data.csv")

    # Thông báo thành công
    messagebox.showinfo("Thông báo", f"Đã xóa thành công {len(selected_indices)} dòng.")





# nhớ lấy hàm này cùng để xóa
def try_convert(value, dtype):
    try:
        if pd.api.types.is_numeric_dtype(dtype):
            return float(value) if '.' in value else int(value)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return pd.to_datetime(value)
        else:
            return str(value).strip()  # Loại bỏ khoảng trắng thừa nếu là chuỗi
    except:
        return value


# =============================== KIỂM TRA KIỂU DỮ LIỆU =============================
def validate_input(input_values, df):
    """
    Kiểm tra xem dữ liệu nhập có đúng định dạng của DataFrame hay không.
    :param input_values: Danh sách các giá trị đầu vào từ người dùng.
    :param df: DataFrame hiện tại (để lấy kiểu dữ liệu của từng cột).
    :return: (bool, error_message) - True nếu hợp lệ, False kèm lỗi nếu không hợp lệ.
    """
    for i, (value, dtype) in enumerate(zip(input_values, df.dtypes)):
        try:
            # Kiểm tra kiểu dữ liệu
            if pd.api.types.is_numeric_dtype(dtype):
                float(value)  # Kiểm tra nếu là số
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                pd.to_datetime(value)  # Kiểm tra nếu là ngày/giờ
            else:
                str(value).strip()  # Kiểm tra nếu là chuỗi
        except ValueError:
            return False, f"Dữ liệu nhập vào cột {df.columns[i]} không hợp lệ: {value}"
    return True, ""






# ================================== Hàm THÊM DỮ LIỆU =====================================
def add_new_data(df, tree, control_frame, root):
    import pandas as pd
    import tkinter as tk
    from tkinter import ttk, messagebox

    # Chuyển cột ngày tháng sang kiểu datetime nếu chưa đúng
    for column in df.columns:
        if 'date' in column.lower() or 'ngày' in column.lower():
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce')
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể chuyển đổi cột '{column}' sang kiểu ngày tháng: {e}")


    # Tạo cửa sổ nhỏ để nhập dữ liệu mới
    add_window = tk.Toplevel(root)
    add_window.title("Thêm dữ liệu mới")
    add_window.geometry("600x300")

    # Frame cho các ô nhập liệu
    input_frame = tk.Frame(add_window)
    input_frame.pack(pady=20, padx=10)

    # Tạo các ô nhập liệu tương ứng với các cột
    entry_fields = {}
    columns = list(df.columns)
    row = 0
    col = 0

    for column in columns:
        tk.Label(input_frame, text=f"{column}:").grid(row=row, column=col, padx=5, pady=5, sticky="w")
        entry = tk.Entry(input_frame, width=15)
        entry.grid(row=row, column=col + 1, padx=5, pady=5)
        entry_fields[column] = entry
        col += 2
        if col >= 8:
            col = 0
            row += 1

    # Hàm kiểm tra dữ liệu
    def validate_input(value, column_name, dtype):
        try:
            if pd.api.types.is_numeric_dtype(dtype) or column_name.lower() == 'year':
                # Kiểm tra kiểu số
                num_value = float(value) if '.' in value else int(value)
                if column_name.lower() == 'year' and num_value <= 1950:
                    return False, f"Giá trị của '{column_name}' phải lớn hơn 1950."
            elif pd.api.types.is_datetime64_any_dtype(dtype) or 'date' in column_name.lower():
                # Kiểm tra định dạng ngày tháng
                date_value = pd.to_datetime(value, errors='coerce')  # Chuyển đổi giá trị
                if pd.isnull(date_value):  # Kiểm tra nếu không phải ngày hợp lệ
                    return False, f"Giá trị '{value}' không hợp lệ cho cột '{column_name}', cần nhập ngày tháng hợp lệ (YYYY-MM-DD)."
            else:
                # Kiểm tra chuỗi
                if not value.strip():
                    return False, f"Giá trị cho '{column_name}' không được để trống."
        except ValueError:
            return False, f"Giá trị '{value}' không hợp lệ cho cột '{column_name}'."
        return True, ""


    # Hàm xử lý khi nhấn "Xác nhận"
    def add_action():
        new_data = {}
        for column, entry in entry_fields.items():
            value = entry.get().strip()
            if not value:
                messagebox.showwarning("Thông báo", f"Vui lòng nhập giá trị cho cột '{column}'.")
                return

            # Kiểm tra dữ liệu nhập
            dtype = df[column].dtype
            is_valid, error_message = validate_input(value, column, dtype)
            if not is_valid:
                messagebox.showwarning("Thông báo", error_message)
                return

            new_data[column] = value

        # Thêm dòng mới vào DataFrame
        try:
            new_row = pd.Series(new_data)
            df.loc[len(df)] = new_row

            # Cập nhật TreeView
            display_data(tree, df)

            save_to_csv(df, file_path)

            # Thông báo thành công
            messagebox.showinfo("Thông báo", "Dữ liệu đã được thêm thành công.")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xảy ra lỗi khi thêm dữ liệu: {str(e)}")

    # Hàm thoát cửa sổ thêm dữ liệu
    def cancel_action():
        add_window.destroy()

    # Nút xác nhận và hủy
    button_frame = tk.Frame(add_window)
    button_frame.pack(side="bottom", fill="x", pady=10)

    confirm_button = ttk.Button(button_frame, text="Xác nhận", command=add_action)
    confirm_button.grid(row=0, column=0, padx=10)

    cancel_button = ttk.Button(button_frame, text="Hủy", command=cancel_action)
    cancel_button.grid(row=0, column=1, padx=10)

# Hàm xóa nội dung trong khu vực điều khiển
def clear_control_area(control_frame):
    for widget in control_frame.winfo_children():
        widget.destroy()

# Hàm cập nhật trạng thái
def update_status(message, color="green"):
    status_label.config(text=message, fg=color)

# ============================= HÀM GIAO DIỆN CHÍNH ==================================
def main_interface():
    root = tk.Tk()
    root.title("Quản lý Dữ liệu Âm Nhạc")
    root.configure(bg="white")
    root.state("zoomed")  
    root.geometry("1000x600")  
    root.state("normal")
    
    

    style = ttk.Style()
    style.configure("TFrame", background="white")
    style.configure("TLabel", background="white", foreground="black")
    style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
    style.configure("Treeview.Heading", background="white", foreground="black")

    # Khung chứa dữ liệu Treeview
    frame = ttk.LabelFrame(root, text="Dữ liệu Âm Nhạc từ năm 1950", padding=10, style="TFrame")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Thanh cuộn dọc
    y_scrollbar = tk.Scrollbar(frame, orient="vertical")
    y_scrollbar.pack(side="right", fill="y")

    # Thanh cuộn ngang
    x_scrollbar = tk.Scrollbar(frame, orient="horizontal")
    x_scrollbar.pack(side="bottom", fill="x")

    # Tạo Treeview
    tree = ttk.Treeview(frame, columns=list(data.columns), show="headings", style="Treeview", yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    
    # Cài đặt chiều rộng cột tự động cho phù hợp với khung
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100, stretch=True)  # stretch=True cho phép tự động điều chỉnh chiều rộng cột

    tree.pack(side="left", fill="both", expand=True)

    # Liên kết thanh cuộn với Treeview
    y_scrollbar.config(command=tree.yview)
    x_scrollbar.config(command=tree.xview)
    
    


    


    # Hiển thị dữ liệu ban đầu
    display_page(tree, data, current_page)

    # Khung các nút điều khiển
    button_frame = ttk.LabelFrame(root, text="Chức năng", padding=10)
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    # Nút điều hướng trang
    ttk.Button(button_frame, text="Trang trước", command=lambda: prev_page(tree, data)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Trang tiếp theo", command=lambda: next_page(tree, data)).pack(side="left", padx=5)

    # Nút các chức năng chính
    ttk.Button(button_frame, text="Tìm kiếm", command=lambda: search_data(tree, data, button_frame)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Sắp xếp theo cột", command=lambda: sort_data(tree, data)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Lọc dữ liệu", command=lambda: filter_data(tree, data, button_frame)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Xóa dữ liệu", command=lambda: delete_data(data, tree)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Thêm dữ liệu", command=lambda: add_new_data(data, tree, button_frame, root)).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Biểu đồ", command=lambda: show_chart_list(button_frame)).pack(side="left", padx=5)

    ttk.Button(button_frame, text="Thoát", command=root.quit).pack(side="right", padx=5)

    # Thêm nút "Cập nhật dữ liệu"
    add_update_button(button_frame, data, tree)



    # Khung thông báo (status)
    global status_label
    status_label = tk.Label(root, text="Trạng thái: Đang sẵn sàng", anchor="w", width=50)
    status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    # Bắt đầu giao diện chính
    root.mainloop()

def intro():
    intro_window = tk.Tk()
    intro_window.title("Intro")
    intro_window.geometry("800x600")  # Kích thước cửa sổ intro
    intro_window.configure(bg="white")

    # Đường dẫn tới file WebP
    webp_path = "giphy.webp"

    # Load ảnh động WebP bằng imageio
    webp_frames = imageio.mimread(webp_path, memtest=False)  # Đọc tất cả các frame từ file WebP
    frame_count = len(webp_frames)

    # Chuyển đổi các frame thành định dạng tương thích với Tkinter
    tk_frames = [
        ImageTk.PhotoImage(Image.fromarray(frame).resize((800, 600), Image.Resampling.LANCZOS))
        for frame in webp_frames
    ]

    # Label để hiển thị ảnh động
    webp_label = tk.Label(intro_window, bg="black")
    webp_label.pack(fill="both", expand=True)

    # Hàm hiển thị từng frame
    def update_frame(frame_index):
        webp_label.config(image=tk_frames[frame_index])
        next_frame = (frame_index + 1) % frame_count
        intro_window.after(100, update_frame, next_frame)  

    update_frame(0)  
    intro_window.after(3000, lambda: (intro_window.destroy(), main_interface()))  
    intro_window.mainloop()
    
if __name__ == "__main__":
    intro()
