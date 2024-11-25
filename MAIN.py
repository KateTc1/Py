import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
from datetime import datetime
import random

# Đọc dữ liệu từ file CSV
file_path = 'top_10000_1950-now.csv'
df = pd.read_csv(file_path)

# Xóa các cột "Album Genres"
columns_to_drop = ['Album Genres']
df = df.drop(columns=columns_to_drop, errors='ignore')  # `errors='ignore'` để tránh lỗi nếu cột không tồn tại

# Thêm dữ liệu ngẫu nhiên cho các ô có giá trị bằng 0
for column in df.columns:
    if column == "Track Number":
        df[column] = df[column].apply(lambda x: np.random.randint(1, 16) if x == 0 else x)
    elif column == "Key":
        df[column] = df[column].apply(lambda x: np.random.randint(1, 21) if x == 0 else x)
    elif column == "Danceability":
        df[column] = df[column].apply(lambda x: round(np.random.uniform(0.1, 0.95), 2) if x == 0 else x)
    elif column == "Mode":
        df[column] = df[column].apply(lambda x: np.random.randint(1, 4) if x == 0 else x)
    elif column == "Instrumentalness":
        df[column] = df[column].apply(lambda x: round(np.random.uniform(0.0001, 0.9), 4) if x == 0 else x)
    elif column == "Popularity":
        df[column] = df[column].apply(lambda x: round(np.random.uniform(10, 99), 2) if x == 0 else x)
    # elif pd.api.types.is_numeric_dtype(df[column]):
    #     df[column] = df[column].apply(lambda x: np.random.randint(1, 100) if x == 0 else x)
    # elif pd.api.types.is_string_dtype(df[column]):
    #     df[column] = df[column].apply(lambda x: f"Random_{np.random.randint(1, 100)}" if x == "0" else x)
        
def generate_full_date(date_str):
    try:
        if pd.isna(date_str):
            return date_str

        # Đảm bảo giá trị là chuỗi để xử lý
        date_str = str(date_str).strip()

        # Nếu giá trị là dạng năm, thêm ngày và tháng ngẫu nhiên
        if len(date_str) == 4 and date_str.isdigit():
            year = int(date_str)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Giới hạn ngày hợp lệ trong tháng
            return datetime(year, month, day).strftime('%Y-%m-%d')
        return date_str
    except Exception as e:
        return date_str
    
# Gọi hàm xử lí time
if 'Album Release Date' in df.columns:
    df['Album Release Date'] = df['Album Release Date'].apply(generate_full_date)

# Tách cột trên thành năm riêng
df['Album Release Date'] = pd.to_datetime(df['Album Release Date'], errors='coerce')
df['Year'] = df['Album Release Date'].dt.year

# loại bỏ thời gian
df['Album Release Date'] = pd.to_datetime(df['Album Release Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
# Tạo workbook và worksheet
wb = Workbook()
ws = wb.active
ws.title = "Cleaned Data"

# Thêm dữ liệu đã chỉnh sửa từ DataFrame vào worksheet
for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        cell = ws.cell(row=r_idx, column=c_idx, value=value)
        # Căn giữa dữ liệu trong ô
        cell.alignment = Alignment(horizontal="center", vertical="center")
        # Đặt font in đậm cho hàng tiêu đề
        if r_idx == 1:
            cell.font = Font(bold=True)

# Thiết lập độ rộng cột tự động dựa trên độ dài của dữ liệu
for column in ws.columns:
    max_length = 0
    column_letter = column[0].column_letter  # Lấy ký tự của cột
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column_letter].width = adjusted_width

# Thêm định dạng bảng cho dữ liệu
table = Table(displayName="CleanedDataTable", ref=f"A1:{column_letter}{len(df) + 1}")
style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True, showColumnStripes=False)
table.tableStyleInfo = style
ws.add_table(table)

# Loại bỏ các dòng trùng lặp
df = df.drop_duplicates()

# Lưu file Excel
output_path = 'cleaned_data.xlsx'
wb.save(output_path)

print("Dữ liệu đã được lưu vào file Excel với định dạng:", output_path)
